from django.urls import path
from . import views

urlpatterns = [
    # --- HTML Frontend Routes ---
    path('', views.HomeView.as_view(), name='index'),
    path('movie/<int:tmdb_id>/', views.MovieDetailHTMLView.as_view(), name='movie_detail'),
    path('camera/', views.EmotionCaptureHTMLView.as_view(), name='camera_page'),
    path('category/', views.CategoryHTMLView.as_view(), name='sort'),
    path('genre/', views.GenreHTMLView.as_view(), name='genre'),
    path('genre/<int:genre_id>/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('tv-shows/', views.TVShowHTMLView.as_view(), name='show'),

    # --- JSON API Routes ---
    path('api/movies/popular/', views.PopularMoviesView.as_view(), name='api-movies-popular'),
    path('api/movies/<int:tmdb_id>/', views.MovieDetailView.as_view(), name='api-movie-detail'),
    path('api/emotion/capture/', views.EmotionCaptureView.as_view(), name='api-emotion-capture'),
    path('api/reviews/', views.ReviewListCreateView.as_view(), name='api-reviews-list-create'),
]