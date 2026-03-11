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
    def get_popular_movies(cls, page=1):
        """
        Fetch popular movies. Caches results for 1 hour.
        """
        cache_key = f"tmdb_popular_movies_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        url = f"{cls.BASE_URL}/movie/popular{cls._get_api_key_param()}&language=en-US&page={page}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Cache for 1 hour (3600 seconds)
            cache.set(cache_key, data, 3600)
            return data
            
        return {"error": "Failed to fetch from TMDB", "status_code": response.status_code}

    @classmethod
    def get_movie_details(cls, movie_id):
        """
        Fetch extensive details for a single movie including credits and videos.
        Caches for 24 hours.
        """
        cache_key = f"tmdb_movie_details_{movie_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        url = f"{cls.BASE_URL}/movie/{movie_id}{cls._get_api_key_param()}&append_to_response=credits,videos"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, 86400) # cache for 24 hrs
            return data
            
        return {"error": "Failed to fetch movie details", "status_code": response.status_code}

    @classmethod
    def search_movies(cls, query, page=1):
        """
        Search movies by query string. Caches for 1 hour.
        """
        cache_key = f"tmdb_search_{query.replace(' ', '_')}_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        url = f"{cls.BASE_URL}/search/movie{cls._get_api_key_param()}&query={query}&include_adult=false&language=en-US&page={page}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, 3600)
            return data
            
        return {"error": "Failed to search movies", "status_code": response.status_code}
        
    @classmethod
    def get_genre_list(cls):
        """
        Fetch the mapping of genre IDs to Genre Names.
        Caches for 7 days since genres rarely change.
        """
        cache_key = "tmdb_genre_list"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        url = f"{cls.BASE_URL}/genre/movie/list{cls._get_api_key_param()}&language=en-US"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, 604800) # 7 days
            return data
            
        return {"error": "Failed to fetch genres", "status_code": response.status_code}

    @classmethod
    def get_popular_tv(cls, page=1):
        """
        Fetch popular TV shows. Caches results for 1 hour.
        """
        cache_key = f"tmdb_popular_tv_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        url = f"{cls.BASE_URL}/tv/popular{cls._get_api_key_param()}&language=en-US&page={page}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, 3600)
            return data
            
        return {"error": "Failed to fetch TV from TMDB", "status_code": response.status_code}
