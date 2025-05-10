from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from pokemon.models import PokemonPrediction, ModelPerformance

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.home_url = reverse('home')
        self.login_url = reverse('login')
        self.predict_url = reverse('predict')
        self.dashboard_url = reverse('dashboard')

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pokemon/home.html')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pokemon/login.html')

    def test_predict_view_requires_login(self):
        response = self.client.get(self.predict_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={self.predict_url}')

    def test_dashboard_view_requires_login(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={self.dashboard_url}')

    def test_authenticated_predict_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.predict_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pokemon/predict.html')

    def test_authenticated_dashboard_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pokemon/dashboard.html')