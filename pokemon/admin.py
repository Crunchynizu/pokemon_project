from django.contrib import admin
from .models import PokemonPrediction, ModelPerformance

admin.site.register(PokemonPrediction)
admin.site.register(ModelPerformance)