from django.db import models

# Create your models here.
class Recipe(models.Model):
    """Recipe objects"""
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient objects"""
    name = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return self.name