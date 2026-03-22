"""
views.py — Template-only views. Zero live TMDB API calls.
All data comes from local PostgreSQL via Django ORM.
Context variables are serialized to dicts matching the existing template format.
"""
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db import models

from .models import Movie, Genre, MovieGenre


# ---------------------------------------------------------------------------
# aggressive monkeypatch for schema mismatch
tmdb_id_field = Genre._meta.get_field('tmdb_id')
tmdb_id_field.primary_key = False
tmdb_id_field.unique = True

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

# Ensure Movie is imported for M2M lookup
from .models import Movie
Genre._meta._expire_cache()
Movie._meta._expire_cache()
MovieGenre._meta._expire_cache()

# Monkeypatch Movie to remove fields that don't exist in DB
# Fields known to be missing: director, cast
MISSING_MOVIE_FIELDS = ['director', 'cast']
Movie._meta.local_fields = [f for f in Movie._meta.local_fields if f.name not in MISSING_MOVIE_FIELDS]
for f_name in MISSING_MOVIE_FIELDS:
    if hasattr(Movie, f_name):
        delattr(Movie, f_name)
if hasattr(Movie._meta, '_get_fields_cache'):
    del Movie._meta._get_fields_cache
Movie._meta._expire_cache()

# ---------------------------------------------------------------------------
# Helper: convert a Movie queryset to the dict format templates expect
# ---------------------------------------------------------------------------

def _movie_to_dict(m: Movie) -> dict:
    """Map a Movie model instance → template-compatible dict."""
    return {
        'id':     m.tmdb_id,
        'name':   m.title,
        'rate':   round(m.vote_average, 1),
        'year':   str(m.release_date.year) if m.release_date else '',
        'year_f': str(m.release_date.year) if m.release_date else '',   # TV shows use year_f
        'poster': m.poster_url,
    }


def _format_queryset(qs, limit: int = 20) -> list:
    """Convert a queryset to a list of template dicts, skip any with no tmdb_id."""
    result = []
    for m in qs:
        if m.tmdb_id:
            result.append(_movie_to_dict(m))
        if len(result) >= limit:
            break
    return result


# =============================================================================
#  HOME PAGE
# =============================================================================

class HomeView(TemplateView):
    template_name = 'first.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        bollywood_qs = (
            Movie.objects
            .filter(content_type='movie', language='hi')
            .order_by('-popularity', '-vote_average')
        )
        south_qs = (
            Movie.objects
            .filter(content_type='movie', language__in=['ta', 'te', 'ml', 'kn'])
            .order_by('-popularity', '-vote_average')
        )

        bollywood    = _format_queryset(bollywood_qs, limit=20)
        south_indian = _format_queryset(south_qs,    limit=20)

        # Hero — deduplicated, top 30
        seen, hero = set(), []
        for m in bollywood + south_indian:
            if m['id'] not in seen:
                seen.add(m['id'])
                hero.append(m)
            if len(hero) >= 30:
                break

        context['tit']          = hero
        context['bollywood']    = bollywood
        context['south_indian'] = south_indian
        return context


# =============================================================================
#  MOVIE DETAIL PAGE
# =============================================================================

class MovieDetailHTMLView(TemplateView):
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tmdb_id = self.kwargs.get('tmdb_id')
        movie   = get_object_or_404(Movie, tmdb_id=tmdb_id)

        context['det'] = {
            'id':            movie.tmdb_id,
            'name':          movie.title,
            'release_date':  movie.release_date,
            'director':      {'director': getattr(movie, 'director', 'Unknown')},
            'actor':         {'actor': getattr(movie, 'cast', 'Various')},
            'rate':          round(movie.vote_average, 1),
            'tagline':       getattr(movie, 'tagline', ''),
            'description':   movie.overview,
            'watch_trailer': getattr(movie, 'trailer_url', ''),
            'img':           {'url': movie.poster_url},
            'backdrop':      movie.backdrop_url,
        }
        context['genres'] = [
            {'genre': g.name, 'id': g.tmdb_id}
            for g in movie.genres.all()
        ]
        return context


# =============================================================================
#  GENRE LIST PAGE
# =============================================================================

class GenreHTMLView(TemplateView):
    template_name = 'genre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genres  = (
            Genre.objects
            .filter(movies__isnull=False)
            .distinct()
            .order_by('name')
        )
        context['cat'] = [{'genre_id': g.tmdb_id, 'genre': g.name} for g in genres]
        return context


# =============================================================================
#  GENRE DETAIL PAGE
# =============================================================================

class GenreDetailView(TemplateView):
    template_name = 'genre_detail.html'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        genre_id = self.kwargs.get('genre_id')
        genre    = get_object_or_404(Genre, tmdb_id=genre_id)

        movies_qs = (
            Movie.objects
            .filter(genres__tmdb_id=genre_id, content_type='movie')
            .order_by('-popularity', '-vote_average')
        )
        context['movies']      = _format_queryset(movies_qs, limit=40)
        context['genre_name']  = genre.name
        return context


# =============================================================================
#  TV SHOWS PAGE
# =============================================================================

class TVShowHTMLView(TemplateView):
    template_name = 'Tvshow.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shows_qs = (
            Movie.objects
            .filter(content_type='tv')
            .order_by('-popularity', '-vote_average')
        )
        context['sh'] = _format_queryset(shows_qs, limit=24)
        return context


# =============================================================================
#  CATEGORY PAGE  (static)
# =============================================================================

class CategoryHTMLView(TemplateView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ca'] = [
            {'category_id': 'bollywood',    'title': 'Bollywood',     'desc': 'Popular Hindi movies'},
            {'category_id': 'south_indian', 'title': 'South Indian',  'desc': 'Tamil, Telugu, Malayalam & Kannada'},
            {'category_id': 'top_rated',    'title': 'Top Rated',     'desc': 'Highest rated movies in DB'},
            {'category_id': 'tv_shows',     'title': 'TV Shows',      'desc': 'Popular Indian web series & shows'},
        ]
        return context


# =============================================================================
#  EMOTION CAPTURE PAGE
# =============================================================================

class EmotionCaptureHTMLView(TemplateView):
    template_name = 'emotion_cap.html'