from django.urls import path
from . import views

urlpatterns = [
    path('api/movies/popular/', views.PopularMoviesView.as_view(), name='api-movies-popular'),
    path('api/movies/<int:tmdb_id>/', views.MovieDetailView.as_view(), name='api-movie-detail'),
    path('api/emotion/capture/', views.EmotionCaptureView.as_view(), name='api-emotion-capture'),
    path('api/reviews/', views.ReviewListCreateView.as_view(), name='api-reviews-list-create'),
]