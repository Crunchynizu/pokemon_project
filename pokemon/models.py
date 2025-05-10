from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class PokemonPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon_name = models.CharField(max_length=50, unique=True)
    model_used = models.CharField(max_length=50)
    predicted_class = models.CharField(max_length=20)
    total = models.IntegerField()
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    sp_attack = models.IntegerField()
    sp_defense = models.IntegerField()
    speed = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pokemon_name} - {self.predicted_class}"

    class Meta:
        unique_together = ("pokemon_name", "model_used")

class ModelPerformance(models.Model):
    MODEL_CHOICES = [
        ('best', 'Best Model'),
        ('svc', 'SVC Model'),
        ('dtc', 'Decision Tree'),
        ('rfc', 'Random Forest'),
    ]

    model_name = models.CharField(max_length=20, choices=MODEL_CHOICES, unique=True)
    accuracy = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model_name} - Accuracy: {self.accuracy}%"

    class Meta:
        unique_together = ("model_name", "accuracy")