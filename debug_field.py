import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')
django.setup()

from movie.models import Movie, Genre

# The monkeypatch should have run because views.py is imported in urls.py?
# No, let's run it here manually to test.
print("Initial fields:", [f.name for f in Movie._meta.local_fields])

MISSING_MOVIE_FIELDS = ['director', 'cast']
Movie._meta.local_fields = [f for f in Movie._meta.local_fields if f.name not in MISSING_MOVIE_FIELDS]
Movie._meta._expire_cache()

print("Fields after monkeypatch:", [f.name for f in Movie._meta.local_fields])

try:
    m = Movie.objects.first()
    print("Fetched movie:", m)
    print("Director attr:", getattr(m, 'director', 'MISSING'))
except Exception as e:
    import traceback
    traceback.print_exc()
