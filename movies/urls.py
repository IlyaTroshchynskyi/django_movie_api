"""
    Collect all routes for movie api
"""


from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views


urlpatterns = [
    path('create_review/', views.ReviewCreateView.as_view()),
    path('add_rating/', views.AddStarRatingView.as_view()),
]


router = SimpleRouter()
router.register(r'category', views.CategoryView, basename='category')
router.register(r'actor', views.ActorViews)
router.register(r'director', views.DirectorViews)
router.register(r'genre', views.GenresViews)
router.register(r'movie', views.MovieViews, basename='movie')
router.register(r'create_wishes', views.WishesCreateView,
                basename='create_wishes')
router.register(r'user_wishes', views.WishesRetrieveDeleteView,
                basename='user_wishes')
router.register(r'rating', views.RatingView, basename='rating')


urlpatterns += router.urls
