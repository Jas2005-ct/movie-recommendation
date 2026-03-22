from django.contrib import admin
from .models import Movie, Genre, MovieGenre, Review, WatchHistory, EmotionLog


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display  = ('tmdb_id', 'name')
    search_fields = ('name',)


class MovieGenreInline(admin.TabularInline):
    model  = MovieGenre
    extra  = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display   = ('tmdb_id', 'title', 'content_type', 'language', 'vote_average', 'popularity', 'synced_at')
    list_filter    = ('content_type', 'language')
    search_fields  = ('title', 'tmdb_id', 'director')
    ordering       = ('-popularity',)
    readonly_fields = ('synced_at',)
    inlines        = [MovieGenreInline]


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
