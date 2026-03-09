from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# ==========================================
# Phase 2: Refactored TMDB-based Models
# ==========================================

class Movie(models.Model):
    """
    Stores minimal movie info locally, using TMDB ID as the definitive reference.
    """
    tmdb_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    cache_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (TMDB: {self.tmdb_id})"

class Genre(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Review(models.Model):
    """
    User ratings and reviews linking Django User -> Movie (TMDB ID).
    Includes sentiment score calculated via TextBlob upon save.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Allow null for anonymous sessions temporarily
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(blank=True, null=True)
    sentiment_score = models.FloatField(null=True, blank=True) # From -1.0 to 1.0 (TextBlob)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}* - {self.movie.title}"

class WatchHistory(models.Model):
    """
    Tracks movies the user has opened/watched for collaborative filtering.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-watched_at']

    def __str__(self):
        return f"Watched: {self.movie.title}"

class EmotionLog(models.Model):
    """
    Logs captured emotions from DeepFace mapping to improve dynamic recommendations.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    emotion = models.CharField(max_length=50) # 'happy', 'sad', 'angry'
    captured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emotion: {self.emotion}"
    
