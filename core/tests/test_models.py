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