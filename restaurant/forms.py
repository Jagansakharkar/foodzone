from django import forms
from .models import Dish


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "price", "stock"]
