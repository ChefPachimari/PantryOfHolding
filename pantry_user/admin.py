from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, DietaryRestriction

class DietaryRestrictionAdmin(admin.ModelAdmin):
    model = DietaryRestriction
    
admin.site.register(DietaryRestriction, DietaryRestrictionAdmin)

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