from django.shortcuts import render,get_object_or_404,redirect ,get_list_or_404
from django.http import HttpResponse
from .models import title
from .models import cate,sho,year,casts,actees,direct,comedian,music,Review,genre
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from textblob import TextBlob
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from deepface import DeepFace
import cv2
import os
import numpy as np
import base64
def first(request):
    sort_option = request.GET.get('sort')
    tit = title.objects.filter(year__gte=2005, year__lt=2024)
    tit = tit.order_by('year')
    if sort_option == "year":
        tit = tit.order_by('year')
    elif sort_option == "az":
        tit = tit.order_by('name') 
    return render(request, 'first.html', {'tit': tit})

def old(request):
    sort_option = request.GET.get('sort')
    tit = title.objects.filter(year__lt=2005)
    tit = tit.order_by('year')
    if sort_option == "year":
        tit = tit.order_by('year')
    elif sort_option == "az":
        tit = tit.order_by('name') 
    return render(request,'old.html',{'tit':tit})


def Tvshows(request):
    sort_option = request.GET.get('sort')
    sh = sho.objects.all()
    if sort_option == "year_f":
        sh = sh.order_by('year_f')
    elif sort_option == "az":
        sh = sh.order_by('name') 
    return render(  request, 'Tvshow.html', {'sh': sh})

def camera_pag(request):
    return render(request, "cam.html")

EMOTION_GENRE_MAPPING = {
    'happy': ['Comedy', 'Action', 'Musical'],
    'sad': ['Drama', 'Romance', 'Thriller'],
    'angry': ['Action', 'Adventure', 'Crime'],
    'surprise': ['Adventure', 'Sci-Fi', 'Fantasy'],
    'fear': ['Horror', 'Drama', 'Thriller'],
    'neutral': ['Drama', 'Family', 'Fantasy']
}
def capture_emotion(request):
    emotion_result = None
    movie_recommendations = None  

    if request.method == 'POST' and request.POST.get("image_data"):
        image_data = request.POST["image_data"]
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]  # Get image extension (e.g., png, jpg)
        file_name = f"captured.{ext}"
        file_path = os.path.join("captured_images", file_name)

        # Save the image
        img_data = ContentFile(base64.b64decode(imgstr), name=file_name)
        file_path = default_storage.save(file_path, img_data)

        abs_file_path = os.path.join(default_storage.location, file_path)

        try:
            # Analyze Emotion with DeepFace
            emotion_analysis = DeepFace.analyze(img_path=abs_file_path, actions=['emotion'], enforce_detection=False)
            emotion_result = emotion_analysis[0]['dominant_emotion']

            # Get the genre based on the detected emotion
            genres = EMOTION_GENRE_MAPPING.get(emotion_result, ['Drama', 'Family', 'Fantasy'])  # Default genres

            # Query movies from your database by genre
            
            movie_recommendations  = title.objects.filter(genres__genre__in=genres).distinct()

        except Exception as e:
            emotion_result = "Error: Could not analyze the emotion."

        return render(request, 'emotion_cap.html', {
            'emotion': emotion_result,
            'movies': movie_recommendations  # Pass movie recommendations to the template
        })

    return render(request, 'emotion_cap.html')

def emotion_based_search(request):
    user_text = request.GET.get('emotion', '').strip()
    sentiment_polarity = None
    sentiment_subjectivity = None
    movies = []

    if user_text:
        blob = TextBlob(user_text)
        sentiment_polarity = blob.sentiment.polarity
        sentiment_subjectivity = blob.sentiment.subjectivity
        if sentiment_polarity > 0.7:
            genres = ["Comedy", "Action", "Musical"]
        elif sentiment_polarity > 0.2:
            genres = ["Adventure", "Romance", "Fantasy"]
        elif sentiment_polarity < -0.7:
            genres = ["Drama", "Horror", "Thriller"]
        elif sentiment_polarity < -0.2:
            genres = ["Romance", "Crime", "Sci-Fi"]
        else:
            genres = ["Drama", "Family", "Fantasy"]

        movies = title.objects.filter(genres__genre__in=genres).distinct()

    return render(request, 'emotion_results.html', {
        'user_text': user_text,
        'sentiment_polarity': sentiment_polarity,
        'sentiment_subjectivity': sentiment_subjectivity,
        'movies': movies,
    })


def movie_det(request,id):
    det = get_object_or_404(title, id=id)
    genres = det.genres.all()

    if request.method == "POST":
        rating = request.POST.get("rating")
        review_text = request.POST.get("review_text")

        Review.objects.create(movie=det, rating=rating, review_text=review_text)
        return redirect('mov_detail', id=id)
    reviews = Review.objects.filter(movie=det)

    return render(request, 'details.html', {'det': det,'genres':genres, 'reviews': reviews})

def review(request,id):
    movie = get_object_or_404(title,id=id)
    reviews = Review.objects.filter(movie_id=movie)
    return render(request, 'review.html', {'movie':movie, 'reviews': reviews})



def sho_det(request,id):
    det = get_object_or_404(sho,id=id)
    return render(request, 'sho_det.html', {'det': det})

def search_result(request):
    query = request.GET.get('query', '').strip()
    movies = title.objects.none()
    actresses = actees.objects.none()
    comedians = comedian.objects.none()
    actors = casts.objects.none()
    directors = direct.objects.none()
    music_directors = music.objects.none()
    genres = genre.objects.none()

    if query.isdigit():
        movies = title.objects.filter(year=query)
    elif query:
        movies |= title.objects.filter(name__icontains=query)
        actors = casts.objects.filter(actor__icontains=query)
        if actors.exists():
            movies |= title.objects.filter(actor__in=actors)

        direc = direct.objects.filter(director__icontains=query)
        if direc.exists():
            movies |= title.objects.filter(director__in=direc)

        genres = genre.objects.filter(genre__icontains=query)
        if genres.exists():
            movies |= title.objects.filter(genres__in=genres)

    actresses = actees.objects.filter(actress__icontains=query)
    comedians = comedian.objects.filter(comedian__icontains=query)

    return render(request, 'search_results.html', {
        'movies': movies.distinct(),  
        'actors': actors.distinct(),  
        'directors': directors.distinct(),  
        'genres': genres.distinct(),  
        'music_directors': music_directors.distinct(),  
        'actresses': actresses.distinct(), 
        'comedians': comedians.distinct(), 
        'query': query,
    })

def category(request):
    cat1 = cate()
    cat1.img = 'YEAR.jpg'
    cat1.name = 'Year'
    cat1.a = reverse('ye')

    cat2 = cate()
    cat2.img = 'ACTOR.jpg'
    cat2.name = 'Actor'
    cat2.a = reverse('act')


    cat3 = cate()
    cat3.img = 'DIRECT.jpg'
    cat3.name = 'Director'
    cat3.a = reverse('direct')


    cat4 = cate()
    cat4.img = 'ACTRESS.jpg'
    cat4.name = 'Actress'
    cat4.a = reverse('heroine')

    cat5 = cate()
    cat5.img = 'COMEDIAN.jpg'
    cat5.name = 'COMEDIAN'
    cat5.a = reverse('comedy')

    cat6 = cate()
    cat6.img = 'MUSIC.jpg'
    cat6.name = 'MUSIC'
    cat6.a = reverse('music_d')


    ca = [cat1,cat2,cat3,cat4,cat5,cat6]

    return render(request,'category.html',{'ca':ca})

def year(request):
    years = range(2000, 2025) 
    return render(request, 'year.html', {'years': years})

def year_based(request,year):
    movies = title.objects.filter(year=year)
    return render(request, 'year_b.html', {'movies': movies,'year':year})


def actor(request):
    acts = casts.objects.all()
    return render(request, 'actor.html', {'acts': acts})

def act_det(request,actor_id):
    actor = get_object_or_404(casts, actor_id=actor_id)
    movies = title.objects.filter(actor_id=actor_id)
    return render(request, 'actor_det.html', {'actor': actor,'movies':movies})

def actress(request):
    actes = actees.objects.all()
    return render(request, 'actress.html', {'actes': actes})

def actress_det(request,actress_id):
    actress = get_object_or_404(actees,actress_id=actress_id)
    return render(request, 'actress_detail.html', {'actress': actress,'actress_id':actress_id})

def director(request):
    dir = direct.objects.all()
    return render(request, 'director.html', {'dir': dir})

def direct_det(request,director_id):
    direc = get_object_or_404(direct, director_id=director_id)
    movies = title.objects.filter(director_id=director_id)
    return render(request, 'direct_det.html', {'direc': direc , 'movies' : movies})

def comedians(request):
    com = comedian.objects.all()
    return render(request, 'comedian.html', {'com': com})

def come_det(request,comedian_id):
    com = get_object_or_404(comedian,comedian_id=comedian_id)
    return render(request, 'come_det.html', {'com': com, 'comedian_id' : comedian_id})

def musics(request): 
    mus = music.objects.all()
    return render(request, 'music.html', {'mus': mus})

def musi_det(request,music_id):
    musi = get_object_or_404(music,music_id=music_id)
    return render(request, 'music_det.html', {'musi': musi, 'music_id' : music_id})

def gen(request):
    cat = genre.objects.all()
    return render(request, 'genre.html', {'cat': cat})
def gen_bas(request,genre_id):
    genr = get_object_or_404(genre,genre_id=genre_id)
    movies = genr.movies.all()
    context = {
        'genr': genr,
        'movies': movies,
    }
    return render(request,'gen_based.html',context)









