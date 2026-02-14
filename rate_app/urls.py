from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user_register/", views.user_register, name="user_register"),
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    # movies section
    path("movies/", views.movie_show_all, name="movie_show_all"),
    path("movie_show_one/", views.movie_show_one, name="movie_one"),
    path("movie_delete/", views.movie_delete, name="movie_delete"),
    path("movie_add/", views.movie_add, name="movie_add"),
    # review section
    path("review_add/", views.review_add, name="review_add"),
    path("review_delete/", views.review_delete, name="review_delete"),
]
