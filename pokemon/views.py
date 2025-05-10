from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import PokemonPrediction
from .forms import PokemonPredictionForm, UserRegistrationForm
import joblib
import os
from django.conf import settings
import pandas as pd

def home(request):
    return render(request, 'pokemon/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'pokemon/login.html')
    
    return render(request, 'pokemon/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid registration data.')
            return render(request, 'pokemon/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'pokemon/register.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def predict_view(request):
    csv_path = os.path.join(settings.BASE_DIR, 'pokemon', 'ml_models', 'Pokedex_Cleaned.csv')
    models_path = os.path.join(settings.BASE_DIR, 'pokemon', 'ml_models')
    
    try:
        pokemon_data = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        pokemon_data = pd.read_csv(csv_path, encoding='latin-1')
    
    # Remove duplicates based on Name
    pokemon_data = pokemon_data.drop_duplicates(subset=['Name'])
    
    pokemon_list = pokemon_data[[
        'Name', 
        'Total', 
        'HP', 
        'Attack', 
        'Defense', 
        'Sp.Atk',
        'Sp.Def',
        'Speed'
    ]].to_dict('records')
    
    context = {
        'pokemon_list': pokemon_list
    }
    
    if request.method == 'POST':
        selected_pokemon = request.POST.get('pokemon_select')
        model_choice = request.POST.get('model_choice')
        
        if selected_pokemon:
            pokemon = next((p for p in pokemon_list if p['Name'] == selected_pokemon), None)
            if pokemon:
                context['selected_pokemon'] = pokemon
                
                if 'predict' in request.POST and model_choice:
                    # Load the selected model
                    model_file = f"{model_choice}_model.pkl"
                    model_path = os.path.join(models_path, model_file)
                    
                    try:
                        with transaction.atomic():
                            model = joblib.load(model_path)
                            
                            # Prepare features for prediction - remove Total as it's a sum of other stats
                            features = [
                                pokemon['HP'],
                                pokemon['Attack'],
                                pokemon['Defense'],
                                pokemon['Sp.Atk'],
                                pokemon['Sp.Def'],
                                pokemon['Speed']
                            ]
                            
                            # Make prediction
                            prediction = model.predict([features])[0]
                            context['prediction'] = prediction
                            
                            # Save prediction to database
                            PokemonPrediction.objects.create(
                                user=request.user,
                                pokemon_name=selected_pokemon,
                                model_used=model_choice,
                                predicted_class=prediction,
                                total=pokemon['Total'],
                                hp=pokemon['HP'],
                                attack=pokemon['Attack'],
                                defense=pokemon['Defense'],
                                sp_attack=pokemon['Sp.Atk'],
                                sp_defense=pokemon['Sp.Def'],
                                speed=pokemon['Speed']
                            )
                    
                    except ValueError as e:
                        messages.error(request, f"Error making prediction: {str(e)}")
    
    return render(request, 'pokemon/predict.html', context)

@login_required
def dashboard_view(request):
    # We'll implement the dashboard logic later
    context = {
        'user': request.user,
        'predictions': []  # Will be populated with user's predictions
    }
    return render(request, 'pokemon/dashboard.html', context)