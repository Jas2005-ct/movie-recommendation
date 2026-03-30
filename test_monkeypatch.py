import os
import django
from django.db import models

os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
django.setup()

from movie.models import Movie, Genre, MovieGenre

print(f"Initial Genre PK field: {Genre._meta.pk.name}")
print(f"Initial MovieGenre.genre field_name: {MovieGenre._meta.get_field('genre').remote_field.field_name}")

# Apply aggressive monkeypatch
tmdb_id_field = Genre._meta.get_field('tmdb_id')
tmdb_id_field.primary_key = False

try:
    id_field = Genre._meta.get_field('id')
except:
    id_field = models.AutoField(primary_key=True, name='id', db_column='id')
    id_field.contribute_to_class(Genre, 'id')

id_field.primary_key = True
Genre._meta.pk = id_field
Genre._meta.db_table = 'genre'
MovieGenre._meta.db_table = 'movie_genre'

# Update Foreign Keys
for field in MovieGenre._meta.local_fields:
    if field.name == 'genre':
        field.remote_field.field_name = 'id'

for field in Movie._meta.local_many_to_many:
    if field.name == 'genres':
        field.remote_field.field_name = 'id'

Genre._meta._expire_cache()
MovieGenre._meta._expire_cache()

print(f"New Genre PK field: {Genre._meta.pk.name}")
print(f"New Genre Table: {Genre._meta.db_table}")
print(f"New MovieGenre.genre field_name: {MovieGenre._meta.get_field('genre').remote_field.field_name}")

# Test lookup
g = Genre.objects.filter(tmdb_id=28).first() # Action
if g:
    print(f"Found Genre: {g.name}, ID: {g.id}, PK: {g.pk}")
else:
    # Try inserting if empty
    print("Genre 28 not found - trying create")
    g = Genre.objects.create(tmdb_id=28, name='Action')
    print(f"Created Genre: {g.name}, ID: {g.id}, PK: {g.pk}")
