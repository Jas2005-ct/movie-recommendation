import os
import django
from django.db import connection

os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
django.setup()

def get_columns(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table_name}'")
        return cursor.fetchall()

print(f"Columns for movie_movie: {get_columns('movie_movie')}")
