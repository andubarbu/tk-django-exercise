from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipes')

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls), name='recipe-list'),
]
