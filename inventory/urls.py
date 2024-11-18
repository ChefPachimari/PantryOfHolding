from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PantryViewSet, FoodCategoryViewSet, FoodViewSet

router = DefaultRouter()
router.register(r'pantry', PantryViewSet, basename='pantry')
router.register(r'food-categories', FoodCategoryViewSet, basename='food-category')
router.register(r'foods', FoodViewSet, basename='food')

urlpatterns = [
    path('', include(router.urls)),
]