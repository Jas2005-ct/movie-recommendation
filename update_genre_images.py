import os
import django
from django.core.files import File
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')
django.setup()

from movie.models import Genre

def update_genres():
    static_genres_dir = os.path.join('static', 'images', 'genres')
    if not os.path.exists(static_genres_dir):
        print(f"Directory not found: {static_genres_dir}")
        return

    files = os.listdir(static_genres_dir)
    print(f"Found {len(files)} files in {static_genres_dir}")

    for filename in files:
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            continue
        
        # Extract genre name from filename (e.g., 'science-fiction.png' -> 'science-fiction')
        name_slug = os.path.splitext(filename)[0]
        
        # Try to find the genre. We'll try a few matching strategies.
        genre = None
        
        # Strategy 1: exact slug match
        all_genres = Genre.objects.all()
        for g in all_genres:
            if slugify(g.name) == name_slug:
                genre = g
                break
        
        if not genre:
            # Strategy 2: case-insensitive name match with hyphens replaced by spaces
            potential_name = name_slug.replace('-', ' ')
            genre = Genre.objects.filter(name__iexact=potential_name).first()

        if genre:
            file_path = os.path.join(static_genres_dir, filename)
            print(f"Updating genre '{genre.name}' with image '{filename}'...")
            with open(file_path, 'rb') as f:
                genre.image.save(filename, File(f), save=True)
            print(f"Successfully updated '{genre.name}'.")
        else:
            print(f"Could not find a genre matching filename: {filename}")

if __name__ == "__main__":
    update_genres()
