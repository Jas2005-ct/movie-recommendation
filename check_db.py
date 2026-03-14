import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')
django.setup()
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'genre';
    """)
    rows = cursor.fetchall()
    print("Columns in 'genre':", [row[0] for row in rows])

    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'movie_genre';
    """)
    rows = cursor.fetchall()
    print("Columns in 'movie_genre':", [row[0] for row in rows])
