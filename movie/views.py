"""
views.py — Template-only views. Zero live TMDB API calls.
All data comes from local PostgreSQL via Django ORM.
Context variables are serialized to dicts matching the existing template format.
"""
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import Movie, Genre


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
        if movie.poster_url:
            context['det'] = {
                'id':            movie.tmdb_id,
                'name':          movie.title,
                'release_date':  movie.release_date,
                'director':      movie.director,
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
        context['cat'] = [{'genre_id': g.id, 'genre': g.name} for g in genres]
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
            from django.db.models import Q
            qs = Movie.objects.filter(
                Q(title__icontains=query) | 
                Q(director__icontains=query) |
                Q(cast__icontains=query)
            ).distinct()
        else:
            qs = Movie.objects.none()

        movies_list, page_obj = _get_paginated_movies(self.request, qs, per_page=24)
        
        context['movies']    = movies_list
        context['page_obj']  = page_obj
        context['query']     = query
        context['count']     = page_obj.paginator.count
        return context


# =============================================================================
#  EMOTION CAPTURE PAGE
# =============================================================================

class EmotionCaptureHTMLView(TemplateView):
    template_name = 'emotion_cap.html'