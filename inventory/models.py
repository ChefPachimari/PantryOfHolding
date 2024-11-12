from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
        Model in case we want to enhance the user down the road
    """

class Pantry(models.Model):
    """ 
        a user's pantry that will contain their inventory
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foods = models.ManyToManyField('Food', related_name='pantries')

    def __str__(self):
        return f"{self.user.username}'s Pantry"
    class Meta:
        verbose_name = 'Pantry'
        verbose_name_plural = 'Pantries'

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
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)

    #overrides
    department = models.CharField(choices=department_choices, max_length=255, null=True, blank=True)
    expiration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name
    