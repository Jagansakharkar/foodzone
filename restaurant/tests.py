from django.test import TestCase

from .models import Meal 
# Create your tests here.
class MealModeTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Meal.objects.create(
      name='Test meal'
      description='This is a test meal',
      price=150
      avaliable=true 
      stock=3
    )
    
    def test_meal_name(self):
      meal=Meal.objects.get(id=1)
      self.assertEqual(meal.name,'Test meal')
      
    def test_stock_count(self):
      meal=Meal.objects.get(id=1)
      
      self.assertEqual(meal.stock,3)