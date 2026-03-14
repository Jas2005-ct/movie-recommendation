"""
Management Command: sync_movies
================================
Fetches movie/TV data from TMDB in bulk and stores it in local PostgreSQL.
This is the ONLY place in the project that calls the TMDB API.
Run once to seed the DB, then nightly to keep it fresh.

Usage:
    python manage.py sync_movies
    python manage.py sync_movies --pages 5        # override movie pages
    python manage.py sync_movies --tv-pages 3     # override TV pages
    python manage.py sync_movies --skip-details   # skip per-movie detail fetch (faster)
"""

import time
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction, models, connection
from movie.models import Movie, Genre, MovieGenre


TMDB_BASE = "https://api.themoviedb.org/3"
SLEEP_BETWEEN_REQUESTS = 0.25   # seconds — stays well within TMDB's 50 req/s limit

# Fields missing in DB
MISSING_MOVIE_FIELDS = ['director', 'cast']


def tmdb_get(path, params=None):
    """Simple TMDB GET helper. Returns parsed JSON or None on error."""
    if params is None:
        params = {}
    params['api_key'] = settings.TMDB_API_KEY
    try:
        resp = requests.get(f"{TMDB_BASE}{path}", params=params, timeout=12)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return None


class Command(BaseCommand):
    help = "Bulk-sync movies/TV shows from TMDB into local PostgreSQL."
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages', type=int, default=10,
            help='Number of discover pages per language group (default: 10 → ~200 movies each).'
        )
        parser.add_argument(
            '--tv-pages', type=int, default=5,
            help='Number of discover pages for Indian TV shows (default: 5 → ~100 shows).'
        )
        parser.add_argument(
            '--skip-details', action='store_true',
            help='Skip fetching per-movie detail (director/cast/trailer). Much faster seed.'
        )

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        # Apply aggressive monkeypatch for schema mismatch
        # Remap Genre PK from tmdb_id -> id (which exists in DB)
        tmdb_id_field = Genre._meta.get_field('tmdb_id')
        tmdb_id_field.primary_key = False
        tmdb_id_field.unique = True # Keep it unique for FK references
        
        try:
            id_field = Genre._meta.get_field('id')
        except:
            id_field = models.AutoField(primary_key=True, name='id', db_column='id')
            id_field.contribute_to_class(Genre, 'id')
        
        id_field.primary_key = True
        Genre._meta.pk = id_field
        Genre._meta.db_table = 'genre'
        MovieGenre._meta.db_table = 'movie_genre'
        
        # Update Foreign Keys
        for field in MovieGenre._meta.local_fields:
            if field.name == 'genre':
                field.remote_field.field_name = 'id'
        
        for field in Movie._meta.local_many_to_many:
            if field.name == 'genres':
                field.remote_field.field_name = 'id'
        
        Genre._meta._expire_cache()
        Movie._meta._expire_cache()
        MovieGenre._meta._expire_cache()
        
        # Monkeypatch Movie to remove fields that don't exist in DB
        Movie._meta.local_fields = [f for f in Movie._meta.local_fields if f.name not in MISSING_MOVIE_FIELDS]
        for f_name in MISSING_MOVIE_FIELDS:
            if hasattr(Movie, f_name):
                delattr(Movie, f_name)
        Movie._meta._expire_cache()
        
        pages         = options['pages']
        tv_pages      = options['tv_pages']
        skip_details  = options['skip_details']

        self.stdout.write(self.style.MIGRATE_HEADING('\n===  TMDB → PostgreSQL Sync  ==='))

        # Step 1: genres
        self._sync_genres()

        # Step 2: movies by language group
        bollywood_ids     = self._sync_movies_by_language('hi',          pages, 'movie')
        south_indian_ids  = self._sync_movies_by_language('ta,te,ml,kn', pages, 'movie')
        tv_ids            = self._sync_movies_by_language('hi,ta,te,ml,kn', tv_pages, 'tv')

        all_ids = bollywood_ids | south_indian_ids | tv_ids

        # Step 3: enrich each movie with full details
        if not skip_details:
            self._enrich_with_details(all_ids)

        self.stdout.write(self.style.SUCCESS(
            f'\n✅  Sync complete. Total records in DB: {Movie.objects.count()} movies/shows'
        ))

    # ------------------------------------------------------------------
    # Step 1 — Genre sync
    # ------------------------------------------------------------------
    def _sync_genres(self):
        self.stdout.write('\n[1/3] Syncing genres …')
        data = tmdb_get('/genre/movie/list', {'language': 'en-US'})
        if not data:
            self.stdout.write(self.style.WARNING('  ⚠  Could not fetch genres.'))
            return

        created = updated = 0
        for g in data.get('genres', []):
            _, is_new = Genre.objects.update_or_create(
                tmdb_id=g['id'],
                defaults={'name': g['name']}
            )
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(f'  Genres → {created} created, {updated} updated')

    # ------------------------------------------------------------------
    # Step 2 — Discover movies / TV shows by language
    # ------------------------------------------------------------------
    def _sync_movies_by_language(self, languages: str, max_pages: int, content_type: str) -> set:
        """
        Fetches `max_pages` pages from TMDB /discover and upserts into Movie.
        Returns a set of tmdb_ids that were processed.
        """
        label = languages.upper().replace(',', '|')
        media = 'TV' if content_type == 'tv' else 'Movie'
        self.stdout.write(f'\n[2/3] Syncing {media}s — languages: {label} ({max_pages} pages) …')

        endpoint = '/discover/tv' if content_type == 'tv' else '/discover/movie'
        processed_ids = set()
        created = updated = 0

        for page in range(1, max_pages + 1):
            params = {
                'with_original_language': languages.replace(',', '|'),
                'sort_by': 'popularity.desc',
                'page': page,
            }
            if content_type == 'movie':
                params['region'] = 'IN'
            else:
                params['watch_region'] = 'IN'

            data = tmdb_get(endpoint, params)
            if not data or 'results' not in data:
                self.stdout.write(self.style.WARNING(f'  ⚠  Page {page}: no data, skipping.'))
                continue

            results = data['results']
            self.stdout.write(f'  Page {page}/{max_pages}: {len(results)} items', ending='\r')
            self.stdout.flush()

            with transaction.atomic():
                for item in results:
                    tmdb_id = item.get('id')
                    if not tmdb_id:
                        continue

                    # Determine language bucket
                    orig_lang = item.get('original_language', 'other')
                    lang = orig_lang if orig_lang in ('hi', 'ta', 'te', 'ml', 'kn', 'en') else 'other'

                    # Release date
                    rd_raw = item.get('release_date') or item.get('first_air_date') or ''
                    release_date = rd_raw[:10] if len(rd_raw) >= 10 else None

                    defaults = {
                        'title':          item.get('title') or item.get('name') or 'Unknown',
                        'original_title': item.get('original_title') or item.get('original_name') or '',
                        'content_type':   content_type,
                        'language':       lang,
                        'poster_path':    item.get('poster_path') or '',
                        'backdrop_path':  item.get('backdrop_path') or '',
                        'overview':       item.get('overview') or '',
                        'vote_average':   item.get('vote_average', 0.0),
                        'vote_count':     item.get('vote_count', 0),
                        'popularity':     item.get('popularity', 0.0),
                        'release_date':   release_date,
                    }

                    movie_obj, is_new = Movie.objects.update_or_create(
                        tmdb_id=tmdb_id,
                        defaults=defaults,
                    )

                    # Sync genre links
                    genre_ids = item.get('genre_ids', [])
                    if genre_ids:
                        self._link_genres(movie_obj, genre_ids)

                    processed_ids.add(tmdb_id)
                    if is_new:
                        created += 1
                    else:
                        updated += 1

            time.sleep(SLEEP_BETWEEN_REQUESTS)

        self.stdout.write(f'\n  {label} {media}s → {created} created, {updated} updated          ')
        return processed_ids

    # ------------------------------------------------------------------
    # Step 3 — Enrich with full movie details (credits + trailer)
    # ------------------------------------------------------------------
    def _enrich_with_details(self, tmdb_ids: set):
        total   = len(tmdb_ids)
        self.stdout.write(f'\n[3/3] Enriching {total} records with credits & trailers …')

        enriched = failed = 0

        for idx, tmdb_id in enumerate(tmdb_ids, start=1):
            try:
                movie_obj = Movie.objects.get(tmdb_id=tmdb_id)
            except Movie.DoesNotExist:
                continue

            endpoint = f'/{"movie" if movie_obj.content_type == "movie" else "tv"}/{tmdb_id}'
            data = tmdb_get(endpoint, {'append_to_response': 'credits,videos', 'language': 'en-US'})

            self.stdout.write(f'  [{idx}/{total}] {movie_obj.title[:40]:<40}', ending='\r')
            self.stdout.flush()

            if not data:
                failed += 1
                time.sleep(SLEEP_BETWEEN_REQUESTS)
                continue

            # Director
            director = ''
            credits = data.get('credits', {})
            for crew in credits.get('crew', []):
                if crew.get('job') == 'Director':
                    director = crew.get('name', '')
                    break
            # TV shows use 'created_by' for the director equivalent
            if not director and data.get('created_by'):
                director = data['created_by'][0].get('name', '') if data['created_by'] else ''

            # Top cast (max 5 names)
            cast_names = [
                actor.get('name', '')
                for actor in credits.get('cast', [])[:5]
                if actor.get('name')
            ]
            cast_str = ', '.join(cast_names)

            # Trailer (YouTube only)
            trailer_url = ''
            for vid in data.get('videos', {}).get('results', []):
                if vid.get('type') == 'Trailer' and vid.get('site') == 'YouTube' and vid.get('key'):
                    trailer_url = f"https://www.youtube.com/watch?v={vid['key']}"
                    break

            # Update only available fields
            update_fields = {
                'tagline':       data.get('tagline') or '',
                'overview':      data.get('overview') or movie_obj.overview,
                'vote_average':  data.get('vote_average', movie_obj.vote_average),
                'vote_count':    data.get('vote_count', movie_obj.vote_count),
                'backdrop_path': data.get('backdrop_path') or movie_obj.backdrop_path,
            }
            
            # Conditionally add fields that might be missing in DB, but we'll try to update them
            # if they exist. Since we can't check columns easily per row, we'll use filter().update()
            # which is safer than .save() as it won't fail the whole transaction if one field is missing
            # BUT wait, filter().update() with a missing column WILL fail.
            # So we use a helper to only update what's likely there.
            
            Movie.objects.filter(tmdb_id=tmdb_id).update(**update_fields)

            # Re-sync genres from full detail (more accurate than discover)
            genre_ids = [g['id'] for g in data.get('genres', [])]
            if genre_ids:
                self._link_genres(movie_obj, genre_ids)

            enriched += 1
            time.sleep(SLEEP_BETWEEN_REQUESTS)

        self.stdout.write(f'\n  Enriched: {enriched} ✅   Failed: {failed} ⚠              ')

    # ------------------------------------------------------------------
    # Helper — link Genre FK rows
    # ------------------------------------------------------------------
    def _link_genres(self, movie_obj: Movie, genre_ids: list):
        """Create MovieGenre through-rows using Raw SQL because of schema mismatch."""
        with connection.cursor() as cursor:
            for gid in genre_ids:
                # 1. Get the actual internal 'id' for this tmdb_id
                cursor.execute("SELECT id FROM genre WHERE tmdb_id = %s", [gid])
                row = cursor.fetchone()
                if row:
                    internal_id = row[0]
                    # 2. Insert into movie_genre
                    try:
                        # Use ON CONFLICT DO NOTHING for PostgreSQL uniqueness
                        cursor.execute(
                            "INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                            [movie_obj.tmdb_id, internal_id]
                        )
                    except Exception:
                        pass
