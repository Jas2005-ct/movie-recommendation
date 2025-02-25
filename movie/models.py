from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from PIL import Image
# Create your models here.

class casts(models.Model):
    actor_id = models.AutoField(primary_key=True)
    actor = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    debut_movie = models.TextField()
    debut_year = models.IntegerField()
    img = models.ImageField(upload_to='pics')

    class Meta:
        managed = False
        db_table = 'casts'
    
class genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=255)
    img = models.ImageField(upload_to='pics')

class direct(models.Model):
    director_id = models.AutoField(primary_key=True)
    director = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    debut_movie = models.TextField()
    debut_year = models.IntegerField()
    img = models.ImageField(upload_to='pics')
    
class title(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    rate = models.FloatField(default=0.0)
    year = models.IntegerField()
    director = models.ForeignKey(direct, null=True, blank=True,on_delete=models.CASCADE,db_column='director_id')
    actor = models.ForeignKey(casts, null=True, blank=True,on_delete=models.CASCADE,db_column='actor_id')
    release_date = models.DateField(null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    watch_trailer = models.URLField(max_length=500, null=True, blank=True)
    genres = models.ManyToManyField('genre', blank=True, related_name='movies')
    def __str__(self):
        return self.name


class cate():
    img: str
    a: str
    name: str

class sho(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    rate = models.FloatField(default=0.0)
    year_f = models.IntegerField()
    ep = models.IntegerField()
    genre = models.CharField(max_length=100, null=True, blank=True) 
    description = models.TextField(null=True, blank=True) 
    streaming_platform = models.CharField(max_length=100, null=True, blank=True) 
    language = models.CharField(max_length=50, null=True, blank=True)  
    trailer_link = models.URLField(null=True, blank=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.img.path)
        desired_size = (200, 300)  
        img.thumbnail(desired_size, Image.ANTIALIAS)
        canvas = Image.new("RGB", desired_size, (255, 255, 255))  
        offset = (
            (desired_size[0] - img.size[0]) // 2,
            (desired_size[1] - img.size[1]) // 2,
        )
        canvas.paste(img, offset)
        canvas.save(self.img.path)


class year():
    year: int

class actees(models.Model):
    actress_id = models.AutoField(primary_key=True)
    actress = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    debut_movie = models.TextField()
    debut_year = models.IntegerField()
    img = models.ImageField(upload_to='pics')



class comedian(models.Model):
    comedian_id = models.AutoField(primary_key=True)
    comedian = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    debut_movie = models.TextField()
    debut_year = models.IntegerField()
    img = models.ImageField(upload_to='pics')

class music(models.Model):
    music_id = models.AutoField(primary_key=True)
    music = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    debut_movie = models.TextField()
    debut_year = models.IntegerField()
    img = models.ImageField(upload_to='pics')

class Review(models.Model):
    movie = models.ForeignKey(title, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # Ensures rating is between 1 and 5
    )
    review_text = models.TextField(blank=True, null=True)  # Optional review text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.movie.name} - {self.rating} Stars"
    
class MovieTitleGenres(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.ForeignKey(title, models.DO_NOTHING)
    genre = models.ForeignKey(genre, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'movie_title_genres'
        unique_together = (('title', 'genre'),)