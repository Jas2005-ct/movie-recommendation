from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# =============================================================================
# REFERENCE / LOOKUP TABLES
# =============================================================================

class Genre(models.Model):
    """
    TMDB genre reference table. Populated once by sync_movies command.
    e.g. id=28 → 'Action', id=18 → 'Drama'
    """
    id  = models.IntegerField(primary_key=True)
    name     = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table         = 'genre'
        verbose_name     = 'Genre'
        verbose_name_plural = 'Genres'
        ordering         = ['name']

    def __str__(self):
        return self.name


# =============================================================================
# CORE CONTENT TABLES
# =============================================================================

class Movie(models.Model):
    """
    Full local mirror of TMDB movie/TV-show data.
    Populated and refreshed exclusively by the `sync_movies` management command.
    Views NEVER call the TMDB API — they only query this table.
    """

    LANGUAGE_CHOICES = [
        ('hi', 'Hindi'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
        ('ml', 'Malayalam'),
        ('kn', 'Kannada'),
        ('en', 'English'),
        ('other', 'Other'),
    ]

    CONTENT_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('tv',    'TV Show'),
    ]

    # ------------------------------------------------------------------
    # Primary key — TMDB ID is our canonical identifier
    # ------------------------------------------------------------------
    tmdb_id      = models.IntegerField(primary_key=True)

    # ------------------------------------------------------------------
    # Core fields (always populated)
    # ------------------------------------------------------------------
    title        = models.CharField(max_length=512)
    original_title = models.CharField(max_length=512, blank=True, default='')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='movie', db_index=True)
    language     = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='other', db_index=True)

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------
    poster_path   = models.CharField(max_length=255, blank=True, default='')
    backdrop_path = models.CharField(max_length=255, blank=True, default='')

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------
    overview      = models.TextField(blank=True, default='')
    tagline       = models.CharField(max_length=512, blank=True, default='')
    release_date  = models.DateField(null=True, blank=True)
    vote_average  = models.FloatField(default=0.0, db_index=True)
    vote_count    = models.IntegerField(default=0)
    popularity    = models.FloatField(default=0.0, db_index=True)

    # ------------------------------------------------------------------
    # Credits (denormalised for simple template rendering)
    # ------------------------------------------------------------------
    director = models.CharField(max_length=255, blank=True, default='')
    cast     = models.TextField(blank=True, default='')   # comma-separated top-3 actors
    trailer_url = models.URLField(max_length=512, blank=True, default='')

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    genres = models.ManyToManyField(
        Genre,
        through='MovieGenre',
        related_name='movies',
        blank=True,
    )

    # ------------------------------------------------------------------
    # Housekeeping
    # ------------------------------------------------------------------
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering  = ['-popularity']
        indexes   = [
            models.Index(fields=['content_type', 'language']),
            models.Index(fields=['content_type', 'popularity']),
        ]

    def __str__(self):
        return f"{self.title} ({self.content_type.upper()}, TMDB:{self.tmdb_id})"

    # ------------------------------------------------------------------
    # Helpers used by templates
    # ------------------------------------------------------------------
    @property
    def poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return ''

    @property
    def backdrop_url(self):
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return ''

    @property
    def year(self):
        return self.release_date.year if self.release_date else ''

    @property
    def cast_list(self):
        """Return cast as a Python list."""
        return [a.strip() for a in self.cast.split(',') if a.strip()]


class MovieGenre(models.Model):
    """
    Explicit through-table for Movie ↔ Genre M2M.
    Allows us to add extra fields (e.g. primary_genre flag) later.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_index=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table         = 'movie_genre'
        verbose_name     = 'Movie Genre'
        verbose_name_plural = 'Movie Genres'
        unique_together  = ('movie', 'genre')
        ordering         = ['movie__title', 'genre__name']

    def __str__(self):
        return f"{self.movie.title} → {self.genre.name}"


# =============================================================================
# USER INTERACTION TABLES
# =============================================================================

class Review(models.Model):
    """
    User ratings and text reviews.
    Sentiment score is calculated via TextBlob when the review is created.
    """
    user         = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    movie        = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating       = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text  = models.TextField(blank=True, default='')
    sentiment_score = models.FloatField(null=True, blank=True)   # -1.0 to +1.0 (TextBlob)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review {self.rating}★ — {self.movie.title}"


class WatchHistory(models.Model):
    """
    Tracks which movies a user has opened/watched.
    Used for collaborative-filtering recommendations.
    """
    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='watch_history')
    movie      = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watch_history')
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-watched_at']

    def __str__(self):
        return f"{self.user} watched {self.movie.title}"


class EmotionLog(models.Model):
    """
    Logs DeepFace-detected emotions to improve dynamic recommendations.
    """
    EMOTION_CHOICES = [
        ('happy',    'Happy'),
        ('sad',      'Sad'),
        ('angry',    'Angry'),
        ('fearful',  'Fearful'),
        ('disgusted','Disgusted'),
        ('surprised','Surprised'),
        ('neutral',  'Neutral'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='emotion_logs')
    emotion     = models.CharField(max_length=50, choices=EMOTION_CHOICES, db_index=True)
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-captured_at']

    def __str__(self):
        return f"Emotion: {self.emotion} ({self.captured_at:%Y-%m-%d})"
