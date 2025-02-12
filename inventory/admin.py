from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Food, Pantry, User, FoodCategory, PantryItem, DietaryRestriction



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

@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(admin.ModelAdmin):
    pass
class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Dietary Restrictions', {'fields': ('dietary_restrictions',)}),
    )
admin.site.register(User, UserAdmin)