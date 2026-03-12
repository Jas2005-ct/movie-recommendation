"""
views.py — Template-only views. Zero live TMDB API calls.
All data comes from local PostgreSQL via Django ORM.
Context variables are serialized to dicts matching the existing template format.
"""
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

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
            'director':      {'director': movie.director},
            'actor':         {'actor': movie.cast},
            'rate':          round(movie.vote_average, 1),
            'tagline':       movie.tagline,
            'description':   movie.overview,
            'watch_trailer': movie.trailer_url,
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