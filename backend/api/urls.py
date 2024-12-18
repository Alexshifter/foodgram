from django.urls import include, path, re_path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from api.recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from api.users.views import NewUserViewSet

api_router = DefaultRouter()

api_router.register('users', NewUserViewSet, basename='users')
api_router.register('tags', TagViewSet, basename='tags')
api_router.register('recipes', RecipeViewSet, basename='recipes')
api_router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(api_router.urls)),
    re_path(r'^auth/token/login/?$', TokenCreateView.as_view(),
            name='login'),
    re_path(r'^auth/token/logout/?$', TokenDestroyView.as_view(),
            name='logout'),
]
