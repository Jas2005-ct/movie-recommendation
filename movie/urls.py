from django.urls import path
from . import views

urlpatterns = [
    # --- HTML Frontend Routes (DB-backed, no live API calls) ---
    path('',                          views.HomeView.as_view(),             name='index'),
    path('movie/<int:tmdb_id>/',      views.MovieDetailHTMLView.as_view(),  name='movie_detail'),
    path('camera/',                   views.EmotionCaptureHTMLView.as_view(), name='camera_page'),
    path('category/',                 views.CategoryHTMLView.as_view(),     name='sort'),
    path('genre/',                    views.GenreHTMLView.as_view(),        name='genre'),
    path('genre/<int:genre_id>/',     views.GenreDetailView.as_view(),      name='genre_detail'),
    path('tv-shows/',                 views.TVShowHTMLView.as_view(),       name='show'),
    path('tv-shows/<int:tmdb_id>/',   views.TVShowDetailView.as_view(),     name='show_details'),
    path('movies/',                   views.MovieListView.as_view(),        name='movie_list'),
    path('movies/<str:category>/',    views.MovieListView.as_view(),        name='movie_list_category'),
    path('search/',                   views.MovieSearchView.as_view(),      name='search_results'),
    path('api/search-suggestions/',   views.SearchResultsAjaxView.as_view(), name='search_suggestions'),
    path('api/reviews/',              views.ReviewCreateView.as_view(),     name='add_review'),
]