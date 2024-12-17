from django.test import TestCase

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', name='Test User')
        assert user.email == 'test@example.com'
        assert user.name == 'Test User'
        assert user.is_active == True
        assert user.is_admin == False

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='test@example.com', name='Test User', password='password')
        assert user.email == 'test@example.com'
        assert user.name == 'Test User'
        assert user.is_active == True
        assert user.is_admin == True

@pytest.mark.django_db
class TestUserViews:
    def test_register_user(self):
        client = APIClient()
        data = {'email': 'test@example.com', 'name': 'Test User', 'password': 'password'}
        response = client.post('/api/register/', data, format='json')
        assert response.status_code == 201
        assert 'token' in response.data
        assert 'name' in response.data
        assert 'email' in response.data

    def test_login_user(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        client = APIClient()
        data = {'email': 'test@example.com', 'password': 'password'}
        response = client.post('/api/login/', data, format='json')
        assert response.status_code == 200
        assert 'token' in response.data
        assert 'name' in response.data
        assert 'email' in response.data

    def test_logout_user(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/api/logout/')
        assert response.status_code == 200
        assert 'message' in response.data

    def test_profile_view(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/profile/')
        assert response.status_code == 200
        assert 'email' in response.data
        assert 'name' in response.data
    
    def test_login_user_invalid_credentials(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        client = APIClient()
        data = {'email': 'test@example.com', 'password': 'wrong_password'}
        response = client.post('/api/login/', data, format='json')
        assert response.status_code == 401
        assert 'error' in response.data
        assert response.data['error'] == 'Credenciais inválidas'

    def test_login_user_non_existent_user(self):
        client = APIClient()
        data = {'email': 'non_existent_user@example.com', 'password': 'password'}
        response = client.post('/api/login/', data, format='json')
        assert response.status_code == 401
        assert 'error' in response.data
        assert response.data['error'] == 'Credenciais inválidas'

    def test_register_user_invalid_email(self):
        client = APIClient()
        data = {'email': 'invalid_email', 'name': 'Test User', 'password': 'password'}
        response = client.post('/api/register/', data, format='json')
        assert response.status_code == 400
        assert 'email' in response.data
        assert response.data['email'] == ['Enter a valid email address.'] 


    def test_register_user_duplicate_email(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        client = APIClient()
        data = {'email': 'test@example.com', 'name': 'Test User', 'password': 'password'}
        response = client.post('/api/register/', data, format='json')
        assert response.status_code == 400
        assert 'email' in response.data
        assert response.data['email'] == ['user with this email already exists.']