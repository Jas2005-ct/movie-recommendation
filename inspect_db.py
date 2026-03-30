import os
import django
from django.db import connection

os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
django.setup()

def get_columns(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table_name}'")
        return cursor.fetchall()

def get_constraints(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT conname, pg_get_constraintdef(c.oid)
            FROM pg_constraint c
            JOIN pg_namespace n ON n.oid = c.connamespace
            WHERE conrelid = '{table_name}'::regclass
        """)
        return cursor.fetchall()

print("--- genre ---")
for col in get_columns('genre'):
    print(col)
print("\n--- genre constraints ---")
for con in get_constraints('genre'):
    print(con)

print("\n--- movie_genre ---")
for col in get_columns('movie_genre'):
    print(col)
print("\n--- movie_genre constraints ---")
for con in get_constraints('movie_genre'):
    print(con)

print("\n--- movie_movie ---")
for col in get_columns('movie_movie'):
    print(col)
