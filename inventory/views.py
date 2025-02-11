from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pantry, FoodCategory, Food
from .serializers import PantrySerializer, FoodCategorySerializer, FoodSerializer
from .filters import FoodFilter

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

class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = FoodSerializer
    queryset = Food.objects.all()  # is there a way to optimize this for performance?
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = FoodFilter
    search_fields = ['name', 'brand']  # Adjust fields as necessary
    lookup_field = 'upc'
    
    def retrieve(self, request, upc=None):
        try:
            # look up food by the UPC which is the cross dataset UID
            food = Food.objects.get(upc=pk)
        except Food.DoesNotExist:
            # TODO: this needs to be reconciled somehow between data sets for for now the current use case is Kroger's API and OpenFoodFacts
            # the object doesn't exist in our database yet so we'll create it
            from .kroger import KrogerAPI  # Assuming you have a KrogerAPI class to handle Kroger's API

            kroger_api = KrogerAPI()
            kroger_object = kroger_api.get_products(upc)
            # TODO: What to do if multiple products are returned?
            if food_data:
                for image in food_data[0]['images']:
                    if image['perspective'] == 'front':
                        thumbnail = image['medium']
                        break
                else:
                    thumbnail = None  # Default to None if no 'front' perspective image is found

                food = Food.objects.create(
                    upc=food_data[0]['upc'],
                    name=food_data[0]['name'],
                    brand=food_data[0]['brand'],
                    food_icon=thumbnail,
                    category=FoodCategory.objects.get_or_create(name=food_data[0]['categories'])[0],
                    # Add other fields as necessary
                )
                return Response(FoodSerializer(food).data)
            
