from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PokemonPredictionForm(forms.Form):
    MODEL_CHOICES = [
        ('best', 'Best Model'),
        ('svc', 'SVC Model'),
        ('dtc', 'Decision Tree'),
        ('rfc', 'Random Forest'),
    ]
    
    model_choice = forms.ChoiceField(choices=MODEL_CHOICES)
    total = forms.IntegerField(min_value=0)
    hp = forms.IntegerField(min_value=0)
    attack = forms.IntegerField(min_value=0)
    defense = forms.IntegerField(min_value=0)
    sp_attack = forms.IntegerField(min_value=0)
    sp_defense = forms.IntegerField(min_value=0)
    speed = forms.IntegerField(min_value=0)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']