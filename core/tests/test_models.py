from core import models
from django.test import TestCase


class ModelsTests(TestCase):
    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Gazpacho',
            description='sopa fría con aceite de oliva, hortalizas crudas, tomates, pepinos, pimientos, cebollas y ajo'
        )
        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test ingredient string representation and """
        recipe = models.Recipe.objects.create(name='Sample recipe', description='sample recipe decription')
        ingredient = models.Ingredient.objects.create(
            name='Tomato',
            recipe=recipe
        )
        self.assertEqual(str(ingredient), ingredient.name)