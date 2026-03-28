from django.conf import settings
import requests
TMDB_BASE = "https://api.themoviedb.org/3"

def tmdb_get(path, params=None):
    """Simple TMDB GET helper. Returns parsed JSON or None on error."""
    if params is None:
        params = {}
    params['api_key'] = settings.TMDB_API_KEY
    try:
        resp = requests.get(f"{TMDB_BASE}{path}", params=params, timeout=12)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return None

