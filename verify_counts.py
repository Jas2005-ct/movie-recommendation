import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
django.setup()

from movie.models import Person, MovieCrew, Movie

print(f"Movies: {Movie.objects.count()}")
print(f"Persons: {Person.objects.count()}")
print(f"MovieCrew: {MovieCrew.objects.count()}")

# Show some examples
for mc in MovieCrew.objects.all()[:5]:
    print(f"  {mc.movie.title} - {mc.person.name} ({mc.role})")
