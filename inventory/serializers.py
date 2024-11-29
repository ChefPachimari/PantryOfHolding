from rest_framework import serializers
from .models import Pantry, FoodCategory, Food, PantryItem

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id', 'name', 'department', 'expiration_time', 'storage')

class FoodSerializer(serializers.ModelSerializer):
    category = FoodCategorySerializer(read_only=True)
    
    # since this is purely for retrieval we put the logic here.  As opposed to the model.abs
    # if we were modifying the inbound data it fits better in the model
    department = serializers.SerializerMethodField()
    expiration = serializers.SerializerMethodField()

    def get_expiration(self, obj):
        if obj.expiration is not None:
            # Convert seconds to days, rounding up to nearest day
            seconds = obj.expiration
            days = round(seconds / (24 * 60 * 60))
            return days
        if obj.category and obj.category.expiration_time is not None:
            return obj.category.expiration_time
        return None

    def get_department(self, obj):
        if obj.category:
            return obj.category.department
        if obj.category and obj.category.department is not None:
            return obj.category.department
        return None

    class Meta:
        model = Food
        fields = ('id', 'name', 'brand', 'category', 'department', 'expiration', 'food_icon')
        read_only_fields = fields
    
    def to_representation(self, instance):
        """
            Used to make some modifications convert `expiration` from seconds to days
        """
        data = super().to_representation(instance)
        if 'expiration' in data and data['expiration'] is not None:

        return data

class PantryItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    class Meta:
        model = PantryItem
        fields = ('id', 'food', 'amount', 'purchase_date', 'purchase_price', 'purchase_location')
        read_only_fields = fields
    
class PantrySerializer(serializers.ModelSerializer):
    pantry_items = PantryItemSerializer(many=True, read_only=True)
    class Meta:
        model = Pantry
        fields = ('id', 'user', 'pantry_items')
        read_only_fields = fields
        