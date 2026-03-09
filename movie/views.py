from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .models import Movie, Review, WatchHistory, EmotionLog
from .serializers import MovieSerializer, ReviewSerializer, WatchHistorySerializer, EmotionLogSerializer
from .services.tmdb import TMDBService
from .services.recommendation_engine import RecommendationEngine

class PopularMoviesView(APIView):
    """
    Returns a list of popular movies directly from TMDB API (Cached).
    """
    def get(self, request):
        page = request.query_params.get('page', 1)
        data = TMDBService.get_popular_movies(page=page)
        
        if "error" in data:
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(data, status=status.HTTP_200_OK)

class MovieDetailView(APIView):
    """
    Fetches full movie details including credits from TMDB.
    Also logs WatchHistory if the user is authenticated.
    """
    def get(self, request, tmdb_id):
        data = TMDBService.get_movie_details(tmdb_id)
        
        if "error" in data:
            return Response(data, status=status.HTTP_404_NOT_FOUND)
            
        # Log to WatchHistory if user is logged in
        if request.user.is_authenticated:
            # Upsert movie locally to fulfill Foreign Key constraint
            title = data.get('title', 'Unknown')
            poster = data.get('poster_path', '')
            release_date = data.get('release_date', None)
            
            movie, _ = Movie.objects.update_or_create(
                tmdb_id=tmdb_id,
                defaults={'title': title, 'poster_path': poster, 'release_date': release_date}
            )
            WatchHistory.objects.create(user=request.user, movie=movie)
            
        return Response(data, status=status.HTTP_200_OK)

class EmotionCaptureView(APIView):
    """
    Accepts a base64 image, uses DeepFace to detect emotion, logs it,
    and returns TMDB movie recommendations biased towards that emotion.
    """
    def post(self, request):
        image_data = request.data.get("image_data")
        if not image_data:
            return Response({"error": "No image_data provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Save the image temporarily to run DeepFace
            format_str, imgstr = image_data.split(';base64,')
            ext = format_str.split('/')[-1]
            file_name = f"captured_api.{ext}"
            file_path = os.path.join("captured_images", file_name)
            
            img_content = ContentFile(base64.b64decode(imgstr), name=file_name)
            saved_path = default_storage.save(file_path, img_content)
            abs_file_path = default_storage.path(saved_path)
            
            emotion_result = "neutral"
            
            try:
                from deepface import DeepFace
                emotion_analysis = DeepFace.analyze(img_path=abs_file_path, actions=['emotion'], enforce_detection=False)
                if isinstance(emotion_analysis, list):
                    emotion_result = emotion_analysis[0]['dominant_emotion']
                else:
                    emotion_result = emotion_analysis['dominant_emotion']
            except ImportError:
                # If deepface is not available on production/deployment machine
                pass
            finally:
                # Clean up the file
                if default_storage.exists(saved_path):
                    default_storage.delete(saved_path)

            # Log emotion
            if request.user.is_authenticated:
                EmotionLog.objects.create(user=request.user, emotion=emotion_result)
                
            # Get Recommendations
            recommendations = RecommendationEngine.get_emotion_based_recommendations(emotion_result)
            
            return Response({
                "detected_emotion": emotion_result,
                "recommendation_engine_results": recommendations
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewListCreateView(APIView):
    """
    List all reviews for a movie or create a new review.
    When creating, calculates TextBlob sentiment automatically.
    """
    def get(self, request):
        tmdb_id = request.query_params.get('tmdb_id')
        if not tmdb_id:
            return Response({"error": "Query param tmdb_id required"}, status=status.HTTP_400_BAD_REQUEST)
            
        reviews = Review.objects.filter(movie__tmdb_id=tmdb_id).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        # We need the local movie object first
        tmdb_id = request.data.get('tmdb_id')
        if not tmdb_id:
            return Response({"error": "tmdb_id required in payload"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Ensure the movie exists in our local DB
        # We assume the frontend passed 'title' if it's new
        title = request.data.get('title', 'Unknown Title')
        movie, _ = Movie.objects.get_or_create(tmdb_id=tmdb_id, defaults={'title': title})
        
        text = request.data.get('review_text', '')
        rating = request.data.get('rating')
        if not rating:
            return Response({"error": "rating is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Analyze Sentiment
        sentiment_score = 0.0
        try:
            from textblob import TextBlob
            if text:
                blob = TextBlob(text)
                sentiment_score = blob.sentiment.polarity
        except ImportError:
            pass
            
        # Create Review
        review = Review.objects.create(
            user=request.user if request.user.is_authenticated else None,
            movie=movie,
            rating=int(rating),
            review_text=text,
            sentiment_score=sentiment_score
        )
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
