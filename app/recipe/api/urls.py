from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, TagViewSet


app_name = 'recipe'

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'tags', TagViewSet)
urlpatterns = [
    path('', include(router.urls)),
] 
