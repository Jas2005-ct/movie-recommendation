from django.contrib import admin
from .models import Movie, Genre, MovieGenre, Review, WatchHistory, EmotionLog


# =============================================================================
# GENRE ADMIN
# =============================================================================

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display   = ('id', 'name', 'movie_count')
    search_fields  = ('name',)
    ordering       = ('name',)

    @admin.display(description='# Movies')
    def movie_count(self, obj):
        return obj.movies.count()


# =============================================================================
# MOVIE GENRE (through-table) ADMIN
# =============================================================================

@admin.register(MovieGenre)
class MovieGenreAdmin(admin.ModelAdmin):
    list_display   = ('movie_title', 'genre_name', 'movie_tmdb_id')
    list_filter    = ('genre',)
    search_fields  = ('movie__title', 'genre__name')
    ordering       = ('movie__title', 'genre__name')
    autocomplete_fields = ('movie', 'genre')

    @admin.display(description='Movie', ordering='movie__title')
    def movie_title(self, obj):
        return obj.movie.title

    @admin.display(description='Genre', ordering='genre__name')
    def genre_name(self, obj):
        return obj.genre.name

    @admin.display(description='TMDB ID', ordering='movie__tmdb_id')
    def movie_tmdb_id(self, obj):
        return obj.movie.tmdb_id


# =============================================================================
# MOVIE ADMIN
# =============================================================================

class MovieGenreInline(admin.TabularInline):
    model       = MovieGenre
    extra       = 0
    fields      = ('genre',)
    verbose_name        = 'Genre'
    verbose_name_plural = 'Genres'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display    = ('tmdb_id', 'title', 'content_type', 'language', 'vote_average', 'popularity', 'synced_at')
    list_filter     = ('content_type', 'language')
    search_fields   = ('title', 'tmdb_id', 'director')
    ordering        = ('-popularity',)
    readonly_fields = ('synced_at',)
    inlines         = [MovieGenreInline]


# =============================================================================
# USER INTERACTION ADMINS
# =============================================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('movie', 'user', 'rating', 'sentiment_score', 'created_at')
    list_filter   = ('rating',)
    search_fields = ('movie__title', 'user__username')


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display  = ('user', 'movie', 'watched_at')
    list_filter   = ('watched_at',)
    search_fields = ('movie__title', 'user__username')


@admin.register(EmotionLog)
class EmotionLogAdmin(admin.ModelAdmin):
    list_display  = ('user', 'emotion', 'captured_at')
    list_filter   = ('emotion',)
