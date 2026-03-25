import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
django.setup()

from movie.models import Person

# Check people with biographies (meaning they were synced)
synced_persons = Person.objects.exclude(biography='')
print(f"Persons with biographies: {synced_persons.count()}")

for p in synced_persons[:3]:
    print(f"--- {p.name} (TMDB: {p.tmdb_id}) ---")
    print(f"Gender: {p.gender}")
    print(f"Birthday: {p.birthday}")
    print(f"Popularity: {p.popularity}")
    print(f"Bio[:100]: {p.biography[:100]}...")
    print()

# Check people without biographies but with tmdb_id
not_synced = Person.objects.filter(tmdb_id__isnull=False, biography='')
print(f"Persons with tmdb_id but NO biography: {not_synced.count()}")
for p in not_synced[:3]:
    print(f"  {p.name} (TMDB: {p.tmdb_id})")
