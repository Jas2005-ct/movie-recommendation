from rest_framework import serializers
from .models import Movie, Genre, Review, WatchHistory, EmotionLog
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['tmdb_id', 'title', 'poster_path', 'release_date']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['tmdb_id', 'name']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'movie', 'rating', 'review_text', 'sentiment_score', 'created_at']
        read_only_fields = ['sentiment_score', 'created_at']

class WatchHistorySerializer(serializers.ModelSerializer):
    movie_details = MovieSerializer(source='movie', read_only=True)
    
    class Meta:
        model = WatchHistory
        fields = ['id', 'user', 'movie', 'movie_details', 'watched_at']
        
class EmotionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionLog
        fields = ['id', 'user', 'emotion', 'captured_at']
