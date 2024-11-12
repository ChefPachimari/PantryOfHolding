from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Food, Pantry, User, FoodCategory, PantryItem

@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass

@admin.register(PantryItem)
class PantryItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Pantry)
class PantryAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)