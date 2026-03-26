import time
from django.core.management.base import BaseCommand
from django.db import transaction
from movie.models import Person
from movie.management.commands.get_tmdb import tmdb_get

class Command(BaseCommand):
    help = "Sync detailed person metadata (biography, birthday, etc.) from TMDB."

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit', type=int, default=0,
            help='Limit the number of artists to sync (0 for all).'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n===  Person Details Sync  ==='))
        
        limit = options['limit']
        # Prioritize people who are actually in the MovieCrew table
        persons = (
            Person.objects
            .filter(tmdb_id__isnull=False, movie_roles__isnull=False)
            .distinct()
            .order_by('-popularity', 'name')
        )
        
        if limit > 0:
            persons = persons[:limit]
            
        total = persons.count()
        self.stdout.write(f"Syncing details for {total} prioritized persons...\n")

        success = 0
        failed = 0

        for idx, person in enumerate(persons, start=1):
            self.stdout.write(f"  [{idx}/{total}] {person.name[:30]:<30}", ending='\r')
            self.stdout.flush()

            data = tmdb_get(f'/person/{person.tmdb_id}', {'language': 'en-US'})
            
            if not data:
                failed += 1
                time.sleep(0.2)
                continue

            try:
                with transaction.atomic():
                    person.gender = data.get('gender')
                    # profile_path sometimes comes as None from TMDB if not available
                    person.profile_path = data.get('profile_path') or person.profile_path or ''
                    person.biography = data.get('biography') or person.biography or ''
                    person.birthday = data.get('birthday') if data.get('birthday') else None
                    person.deathday = data.get('deathday') if data.get('deathday') else None
                    person.place_of_birth = data.get('place_of_birth') or person.place_of_birth or ''
                    person.popularity = data.get('popularity', 0.0)
                    person.save()
                success += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\n  Error saving {person.name}: {e}"))
                failed += 1

            # Respect TMDB rate limits (approx 40 reqs per 10 seconds)
            time.sleep(0.25)

        self.stdout.write(self.style.SUCCESS(
            f'\n\n✅  Person sync complete. {success} updated, {failed} failed.'
        ))
