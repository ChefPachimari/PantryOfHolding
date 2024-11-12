from django.shortcuts import render
from rest_framework import viewsets
from .models import Pantry, FoodCategory, Food
from .serializers import PantrySerializer, FoodCategorySerializer, FoodSerializer

class PantryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user's pantry instances.
    """
    serializer_class = PantrySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Pantry.objects.filter(user__id=user_id)
    
class FoodCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = FoodCategorySerializer
    queryset = FoodCategory.objects.all()

class FoodViewSet(viewsets.ModelViewSet):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()