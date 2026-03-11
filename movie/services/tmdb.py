import requests
from django.conf import settings
from django.core.cache import cache

class TMDBService:
    """
    Service layer to interact with The Movie Database (TMDB) API v3.
    It implements caching to reduce redundant network calls and abide by rate limits.
    """
    BASE_URL = "https://api.themoviedb.org/3"
    
    @classmethod
    def _get_headers(cls):
        return {
            "Authorization": f"Bearer {settings.TMDB_API_KEY}" if len(settings.TMDB_API_KEY) > 40 else "",
        }
    
    @classmethod
    def _get_api_key_param(cls):
        # Fallback if they provide the API Key instead of the Bearer Token
        return f"?api_key={settings.TMDB_API_KEY}"

    @classmethod
    def _fetch_data(cls, url, cache_key, timeout_seconds=3600):
        """
        Helper method to fetch data, handle caching, timeouts, and network exceptions.
        """
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
            
        try:
            # We add a 10s timeout to prevent hanging, and catch any connection reset errors
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data, timeout_seconds)
                return data
            return {"error": "TMDB API Error", "status_code": response.status_code}
        except requests.RequestException as e:
            # Instead of crashing the entire Django app with a 500 Server Error,
            # we gracefully return a dictionary indicating a connection failure.
            return {"error": f"Connection Error: {str(e)}"}

    # -----------------------------------------------------------------------
    # General / Global Methods
    # -----------------------------------------------------------------------

    @classmethod
    def get_popular_movies(cls, page=1):
        """
        Fetch popular movies globally. Caches results for 1 hour.
        """
        url = f"{cls.BASE_URL}/movie/popular{cls._get_api_key_param()}&language=en-US&page={page}"
        cache_key = f"tmdb_popular_movies_page_{page}"
        return cls._fetch_data(url, cache_key, 3600)

    @classmethod
    def get_movie_details(cls, movie_id):
        """
        Fetch extensive details for a single movie including credits and videos.
        Caches for 24 hours.
        """
        url = f"{cls.BASE_URL}/movie/{movie_id}{cls._get_api_key_param()}&append_to_response=credits,videos"
        cache_key = f"tmdb_movie_details_{movie_id}"
        return cls._fetch_data(url, cache_key, 86400)

    @classmethod
    def search_movies(cls, query, page=1):
        """
        Search movies by query string. Caches for 1 hour.
        """
        url = f"{cls.BASE_URL}/search/movie{cls._get_api_key_param()}&query={query}&include_adult=false&language=en-US&page={page}"
        cache_key = f"tmdb_search_{query.replace(' ', '_')}_{page}"
        return cls._fetch_data(url, cache_key, 3600)
        
    @classmethod
    def get_genre_list(cls):
        """
        Fetch the mapping of genre IDs to Genre Names.
        Caches for 7 days since genres rarely change.
        """
        url = f"{cls.BASE_URL}/genre/movie/list{cls._get_api_key_param()}&language=en-US"
        cache_key = "tmdb_genre_list"
        return cls._fetch_data(url, cache_key, 604800)

    @classmethod
    def get_movies_by_genre(cls, genre_id, page=1):
        """
        Fetch Indian movies by a specific genre ID. Caches results for 1 hour.
        Filters to Indian region (Bollywood + South Indian combined).
        """
        # hi=Hindi (Bollywood), ta=Tamil, te=Telugu, ml=Malayalam, kn=Kannada
        url = (
            f"{cls.BASE_URL}/discover/movie{cls._get_api_key_param()}"
            f"&with_genres={genre_id}"
            f"&with_original_language=hi|ta|te|ml|kn"
            f"&region=IN&sort_by=popularity.desc&page={page}"
        )
        cache_key = f"tmdb_indian_genre_movies_{genre_id}_page_{page}"
        return cls._fetch_data(url, cache_key, 3600)

    # -----------------------------------------------------------------------
    # Indian / South Indian Specific Methods
    # -----------------------------------------------------------------------

    @classmethod
    def get_indian_movies(cls, page=1):
        """
        Fetch popular Bollywood (Hindi) movies from India. Caches for 1 hour.
        """
        url = (
            f"{cls.BASE_URL}/discover/movie{cls._get_api_key_param()}"
            f"&with_original_language=hi"
            f"&region=IN&sort_by=popularity.desc&page={page}"
        )
        cache_key = f"tmdb_indian_movies_page_{page}"
        return cls._fetch_data(url, cache_key, 3600)

    @classmethod
    def get_south_indian_movies(cls, page=1):
        """
        Fetch popular South Indian movies (Tamil, Telugu, Malayalam, Kannada).
        Caches for 1 hour.
        """
        url = (
            f"{cls.BASE_URL}/discover/movie{cls._get_api_key_param()}"
            f"&with_original_language=ta|te|ml|kn"
            f"&region=IN&sort_by=popularity.desc&page={page}"
        )
        cache_key = f"tmdb_south_indian_movies_page_{page}"
        return cls._fetch_data(url, cache_key, 3600)

    @classmethod
    def get_indian_tv(cls, page=1):
        """
        Fetch popular Indian TV shows (Hindi + South). Caches for 1 hour.
        """
        url = (
            f"{cls.BASE_URL}/discover/tv{cls._get_api_key_param()}"
            f"&with_original_language=hi|ta|te|ml|kn"
            f"&watch_region=IN&sort_by=popularity.desc&page={page}"
        )
        cache_key = f"tmdb_indian_tv_page_{page}"
        return cls._fetch_data(url, cache_key, 3600)

    @classmethod
    def get_popular_tv(cls, page=1):
        """
        Fetch popular TV shows globally. Caches results for 1 hour.
        """
        url = f"{cls.BASE_URL}/tv/popular{cls._get_api_key_param()}&language=en-US&page={page}"
        cache_key = f"tmdb_popular_tv_page_{page}"
        return cls._fetch_data(url, cache_key, 3600)
