from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Pantry, FoodCategory, Food
from .serializers import PantrySerializer, FoodCategorySerializer, FoodSerializer

class PantryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user's pantry instances.
    """
    serializer_class = PantrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        return Pantry.objects.filter(user=self.request.user)
    
class FoodCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = FoodCategorySerializer
    queryset = FoodCategory.objects.all()

class FoodViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = FoodSerializer
    queryset = Food.objects.all()