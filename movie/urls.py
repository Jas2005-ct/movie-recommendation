from django.urls import path
from .import views

urlpatterns = [
    path('',views.first, name='index'),
    path('old/', views.old, name='old_mov'),
    path('search/', views.search_result, name='search_results'),
    path('category/',views.category, name='sort'),
    path('Tvshow/',views.Tvshows,name='show'),
    path('year/int:year/',views.year,name='ye'),
    path('movies/<int:year>/', views.year_based, name='year_b'),
    path('actor/',views.actor,name='act'),
    path('actress/',views.actress,name='heroine'),
    path('director/',views.director,name='direct'),
    path('comedian/',views.comedians,name='comedy'),
    path('musics/',views.musics,name='music_d'),
    path('act_det/<int:actor_id>/', views.act_det, name='acts_detail'),
    path('actress_det/<int:actress_id>',views.actress_det,name='actres_detail'),
    path('direct_det/<int:director_id>',views.direct_det,name='director_detail'),
    path('music_det/<int:music_id>',views.musi_det,name='music_detail'),
    path('come_det/<int:comedian_id>',views.come_det,name='come_detail'),
    path('det/<int:id>/', views.movie_det, name='mov_detail'),
    path('gen', views.gen, name='genre'),
    path('genre/<int:genre_id>/', views.gen_bas, name='genre_movies'),
    path('emotion-search/', views.emotion_based_search, name='emotion_based_search'),
    path('review/<int:id>/', views.review, name='show_review'),
    path('show/<int:id>/', views.sho_det, name='show_det'),
    path('camera/', views.camera_pag, name='camera_page'),
    path('capture-emotion/', views.capture_emotion, name='capture_emotion')
]