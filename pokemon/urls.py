from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='pokemon/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('register/', views.register_view, name='register'),  # Updated to match view name
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('predict/', views.predict_view, name='predict'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]