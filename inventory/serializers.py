from rest_framework import serializers
from .models import Pantry, FoodCategory, Food

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id', 'name', 'department', 'expiration_time', 'storage')

class FoodSerializer(serializers.ModelSerializer):
    category = FoodCategorySerializer(read_only=True)
    
    class Meta:
        model = Food
        fields = ('id', 'name', 'brand', 'category', 'department', 'expiration')
        read_only_fields = fields
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'expiration' in data and data['expiration'] is not None:
            # Convert seconds to days, rounding up to nearest day
            seconds = data['expiration']
            days = round(seconds / (24 * 60 * 60))
            data['expiration'] = days
        return data

class PantrySerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True, read_only=True)
    class Meta:
        model = Pantry
        fields = ('id', 'user', 'foods')
        read_only_fields = fields