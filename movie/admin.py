from django.contrib import admin
from .models import Movie, Genre, Review, WatchHistory, EmotionLog

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(WatchHistory)
admin.site.register(EmotionLog)

