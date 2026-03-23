"""
views.py — Template-only views. Zero live TMDB API calls.
All data comes from local PostgreSQL via Django ORM.
Context variables are serialized to dicts matching the existing template format.
"""
from django.views.generic import TemplateView
from django.db import models
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from textblob import TextBlob
import json
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Movie, Genre, MovieGenre, Review


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
# Fields known to be missing: director, cast, cache_updated_at
MISSING_MOVIE_FIELDS = ['director', 'cast', 'cache_updated_at']
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
        if m.tmdb_id and m.poster_url:
            result.append(_movie_to_dict(m))
        if len(result) >= limit:
            break
    return result


def _get_paginated_movies(request, qs, per_page: int = 24):
    """
    Paginates a queryset. Ensures valid records are filtered at the database level.
    Returns: (list_of_dicts, page_obj)
    """
    # Ensure we only paginate records that have both a TMDB ID and a poster URL
    qs = qs.filter(tmdb_id__isnull=False).exclude(poster_path='')
    
    paginator = Paginator(qs, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Map objects to dicts for template
    result = [_movie_to_dict(m) for m in page_obj.object_list]
            
    return result, page_obj


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
            .order_by('-popularity', '-vote_average')[:20]
        )
        south_qs = (
            Movie.objects
            .filter(content_type='movie', language__in=['ta', 'te', 'ml', 'kn'])
            .order_by('-popularity', '-vote_average')[:20]
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
        
        # Add reviews to context
        try:
            context['reviews'] = movie.reviews.all().order_by('-created_at')
        except Exception as e:
            print(f"Error fetching reviews for {movie.tmdb_id}: {e}")
            context['reviews'] = []
        
        return context


# =============================================================================
#  REVIEW SUBMISSION API
# =============================================================================

class ReviewCreateView(View):
    """
    Handles AJAX POST requests from details.html to save a new review.
    Calculates sentiment score on the fly.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            tmdb_id     = data.get('tmdb_id')
            rating      = data.get('rating')
            review_text = data.get('review_text', '')

            movie = get_object_or_404(Movie, tmdb_id=tmdb_id)

            # Sentiment Analysis
            sentiment = 0.0
            if review_text:
                blob = TextBlob(review_text)
                sentiment = blob.sentiment.polarity

            review = Review.objects.create(
                user=request.user if request.user.is_authenticated else None,
                movie=movie,
                rating=rating,
                review_text=review_text,
                sentiment_score=sentiment
            )

            return JsonResponse({
                'id': review.id,
                'status': 'success',
                'message': 'Review published successfully!'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


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
        context['cat'] = [
            {
                'genre_id': g.id, 
                'genre': g.name, 
                'image_url': g.image.url if g.image else None
            } 
            for g in genres
        ]
        return context


# =============================================================================
#  GENRE DETAIL PAGE
# =============================================================================

class GenreDetailView(TemplateView):
    template_name = 'genre_detail.html'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        genre_id = self.kwargs.get('genre_id')
        genre    = get_object_or_404(Genre, id=genre_id)

        sort_by = self.request.GET.get('sort', 'popularity')
        
        movies_qs = (
            Movie.objects
            .filter(genres__id=genre_id, content_type='movie', tmdb_id__isnull=False)
        )
        
        if sort_by == 'year':
            movies_qs = movies_qs.order_by('-release_date', '-popularity')
        elif sort_by == 'az':
            movies_qs = movies_qs.order_by('-vote_average', '-popularity')
        else:
            movies_qs = movies_qs.order_by('-popularity', '-vote_average')

        movies_list, page_obj = _get_paginated_movies(self.request, movies_qs, per_page=24)
        
        context['movies']      = movies_list
        context['page_obj']    = page_obj
        context['genre_name']  = genre.name
        return context


# =============================================================================
#  TV SHOWS PAGE
# =============================================================================

class TVShowHTMLView(TemplateView):
    template_name = 'Tvshow.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get('sort', 'popularity')
        
        shows_qs = (
            Movie.objects
            .filter(content_type='tv', tmdb_id__isnull=False)
        )
        
        if sort_by == 'year':
            shows_qs = shows_qs.order_by('-release_date', '-popularity')
        elif sort_by == 'az':
            shows_qs = shows_qs.order_by('-vote_average', '-popularity')
        else:
            shows_qs = shows_qs.order_by('-popularity', '-vote_average')

        shows_list, page_obj = _get_paginated_movies(self.request, shows_qs, per_page=24)
        
        context['sh']       = shows_list
        context['page_obj'] = page_obj
        return context

class TVShowDetailView(TemplateView):
    template_name = 'show_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tmdb_id = self.kwargs.get('tmdb_id')
        movie   = get_object_or_404(Movie, tmdb_id=tmdb_id)
        if movie.poster_url:
            context['det'] = {
                'id':            movie.tmdb_id,
                'name':          movie.title,
                'release_date':  movie.release_date,
                'director':      movie.director,
                'music_director': movie.music_director,
                'main_actor':    movie.main_actor,
                'main_actress':  movie.main_actress,
                'villain':       movie.villain,
                'comedian':      movie.comedian,
                'actor':         movie.cast,
                'rate':          round(movie.vote_average, 1),
                'tagline':       movie.tagline,
                'description':   movie.overview,
                'watch_trailer': movie.trailer_url,
                'img':           {'url': movie.poster_url},
                'backdrop':      movie.backdrop_url,
            }
            context['genres'] = [
                {'genre': g.name, 'id': g.id}
                for g in movie.genres.all()
            ]
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
#  MOVIE LIST PAGE (Paginated)
# =============================================================================

class MovieListView(TemplateView):
    template_name = 'movie_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category', 'all')
        sort_by  = self.request.GET.get('sort', 'popularity')
        
        qs = Movie.objects.filter(content_type='movie', tmdb_id__isnull=False)
        
        title = "All Movies"
        if category == 'bollywood':
            qs = qs.filter(language='hi')
            title = "Bollywood Hits"
        elif category == 'south_indian':
            qs = qs.filter(language__in=['ta', 'te', 'ml', 'kn'])
            title = "South Indian Blockbusters"
        elif category == 'top_rated':
            # Skip popularity default if specifically asking for top rated
            qs = qs.order_by('-vote_average', '-popularity')
            title = "Top Rated Movies"

        # Apply sorting if not already handled by top_rated logic
        if category != 'top_rated':
            if sort_by == 'year':
                qs = qs.order_by('-release_date', '-popularity')
            elif sort_by == 'az':
                qs = qs.order_by('-vote_average', '-popularity')
            else:
                qs = qs.order_by('-popularity', '-vote_average')

        movies_list, page_obj = _get_paginated_movies(self.request, qs, per_page=24)
        
        context['movies']    = movies_list
        context['page_obj']  = page_obj
        context['title']     = title
        context['category']  = category
        return context



# =============================================================================
#  SEARCH RESULTS PAGE
# =============================================================================

class MovieSearchView(TemplateView):
    template_name = 'search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '').strip()
        
        if query:
            # Use PostgreSQL Full-Text Search with weighting and ranking
            # Title (A) is weighted highest, then Overview (B)
            vector = SearchVector('title', weight='A') + \
                     SearchVector('overview', weight='B')
            
            search_query = SearchQuery(query)
            
            # Filter and rank results
            qs = Movie.objects.annotate(
                rank=SearchRank(vector, search_query)
            ).filter(rank__gte=0.1).order_by('-rank', '-popularity')
        else:
            qs = Movie.objects.none()

        movies_list, page_obj = _get_paginated_movies(self.request, qs, per_page=24)
        
        context['movies']    = movies_list
        context['page_obj']  = page_obj
        context['query']     = query
        context['count']     = page_obj.paginator.count
        return context


class SearchResultsAjaxView(View):
    """
    Search suggestions for AJAX autocomplete.
    Returns a small JSON list of top matches.
    """
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '').strip()
        if not query or len(query) < 2:
            return JsonResponse({'results': []})

        # Simple but fast search for autocomplete
        # (FTS might be overkill here, icontains is fine for small top-N suggestion)
        results = (
            Movie.objects
            .filter(title__icontains=query)
            .order_by('-popularity')[:8]
        )
        
        data = [
            {
                'id': m.tmdb_id,
                'title': m.title,
                'year': m.release_date.year if m.release_date else '',
                'poster': m.poster_url,
                'url': f"/movie/{m.tmdb_id}/"
            }
            for m in results
        ]
        
        return JsonResponse({'results': data})


# =============================================================================
#  EMOTION CAPTURE PAGE
# =============================================================================

class EmotionCaptureHTMLView(TemplateView):
    template_name = 'emotion_cap.html'