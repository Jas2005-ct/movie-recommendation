import requests
from django.conf import settings
from .tmdb import TMDBService

class RecommendationEngine:
    """
    Hybrid Recommendation Engine combining:
    1. Content-Based Filter (TMDB similar genres)
    2. Emotion-Boosted Recommender (Happy, Sad, Angry)
    """

    # Mapping emotions directly to TMDB Genre IDs
    # Action=28, Comedy=35, Adventure=12, Romance=10749, Thriller=53, Horror=27, Drama=18
    EMOTION_GENRE_MAPPING = {
        'happy': [35, 12, 10749],     # Comedy, Adventure, Romance (Feel-good)
        'sad': [35, 10749, 18],       # Comedy, Romance, Drama 
        'angry': [28, 53, 12],        # Action, Thriller, Adventure
        'surprise': [12, 878, 14],    # Adventure, Sci-Fi, Fantasy
        'fear': [27, 53, 18],         # Horror, Thriller, Drama
        'neutral': [18, 10751, 14]    # Drama, Family, Fantasy
    }

    @classmethod
    def get_similar_movies_from_tmdb(cls, movie_id):
        """
        Content-Based Filtering: Gets similar movies strictly based on a single TMDB ID.
        Uses TMDB's internal similarity algorithm.
        """
        url = f"{TMDBService.BASE_URL}/movie/{movie_id}/similar{TMDBService._get_api_key_param()}&language=en-US&page=1"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {"error": "Failed to fetch similar movies"}

    @classmethod
    def get_emotion_based_recommendations(cls, emotion):
        """
        Takes a detected emotion string (from DeepFace or TextBlob) and converts it 
        to TMDB genre IDs. Then queries TMDB Discover API to return those specific movies.
        """
        target_genres = cls.EMOTION_GENRE_MAPPING.get(emotion.lower(), cls.EMOTION_GENRE_MAPPING['neutral'])
        
        # Convert list of integers to a comma separated string for the API (e.g. "35,12")
        genre_payload = ",".join(map(str, target_genres))
        
        url = f"{TMDBService.BASE_URL}/discover/movie{TMDBService._get_api_key_param()}&language=en-US&sort_by=popularity.desc&with_genres={genre_payload}&page=1"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        return {"error": f"Failed to discover movies for emotion: {emotion}"}

    @classmethod
    def analyze_sentiment(cls, text):
        """
        If TextBlob is installed, this analyzes review text to score it from -1 (Sad) to 1 (Happy).
        Can be used to automatically categorize written reviews.
        """
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.5:
                return 'happy'
            elif polarity < -0.5:
                return 'angry'
            elif polarity < 0:
                return 'sad'
            else:
                return 'neutral'
        except ImportError:
            # Fallback if textblob fails to load
            return 'neutral'
