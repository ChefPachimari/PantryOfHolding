from django.db import models
from django.contrib.auth.models import AbstractUser

class DietaryRestriction(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
        Model in case we want to enhance the user down the road
    """
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(unique=True)
    
    dietary_restrictions_choices = (
        ('none', 'None'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('gluten_free', 'Gluten Free'),
        ('dairy_free', 'Dairy Free'),
        ('nut_free', 'Nut Free'),
        ('halal', 'Halal'),
        ('kosher', 'Kosher'),
    )
    dietary_restrictions = models.ManyToManyField('DietaryRestriction', blank=True)

class Pantry(models.Model):
    """ 
        a user's pantry that will contain their inventory
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pantry_items = models.ManyToManyField('PantryItem', related_name='pantries')

    def __str__(self):
        return f"{self.user.username}'s Pantry"
    class Meta:
        verbose_name = 'Pantry'
        verbose_name_plural = 'Pantries'

class PantryItem(models.Model):
    """
        A food item in a user's pantry
    """
    pantry = models.ForeignKey(Pantry, on_delete=models.CASCADE)
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    units = models.CharField(max_length=255)
    opened = models.BooleanField(default=False)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_location = models.CharField(max_length=255)

    def amount(self):
        return f"{self.quantity} {self.units}"

    def __str__(self):
        return f"{self.food.name} in {self.pantry.user.username}'s Pantry"
    class Meta:
        verbose_name = 'Pantry Item'
        verbose_name_plural = 'Pantry Items'

class FoodCategory(models.Model):
    """
        Gives us some common info for groups of food such similar cuts of meat having the same expiration time frame
        ? Should this be tied in to departments ?
    """
    # storage_choices = ('refrigerator', 'pantry', 'other')
    storage_choices = (
        ('refrigerator', 'Refrigerator'),
        ('pantry', 'Pantry'),
        ('other', 'Other'),
    )
    department_choices = (
        ('produce', 'Produce'),
        ('meat', 'Meat'),
        ('packaged', 'Packaged'),
        ('fish', 'Fish'),
        ('dairy', 'Dairy'),
        ('bakery', 'Bakery'),
        ('freezer', 'Freezer'),
    )
    name = models.CharField(max_length=255)
    department = models.CharField(choices=department_choices, max_length=255)
    expiration_time = models.DurationField()
    storage = models.CharField(choices=storage_choices, max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'

class Food(models.Model):
    """
        Model for the food item, independent from the pantry
    """
    # department_choices = ('produce', 'meat', 'packaged', 'fish', 'dairy', 'bakery', 'freezer')
    department_choices = (
        ('produce', 'Produce'),
        ('meat', 'Meat'),
        ('packaged', 'Packaged'),
        ('fish', 'Fish'),
        ('dairy', 'Dairy'),
        ('bakery', 'Bakery'),
        ('freezer', 'Freezer'),
    )
    # TODO: do we need an internal UUID?
    name = models.CharField(max_length=255)
    upc = models.CharField(max_length=12, unique=True)  # Universal Product Codes are intended to be unique and shouldn't collide so we can unique it
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    food_icon = models.ImageField(upload_to='food_icons/', null=True, blank=True)

    #overrides
    department = models.CharField(choices=department_choices, max_length=255, null=True, blank=True)
    expiration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name
    