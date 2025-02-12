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
    REQUIRED_FIELDS = []
    
    email = models.EmailField(unique=True)
    dietary_restrictions = models.ManyToManyField('DietaryRestriction', blank=True)
