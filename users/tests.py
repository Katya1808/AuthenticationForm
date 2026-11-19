import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestHomeView:
    """Тесты главной страницы."""

    def test_home_page_returns_200(self):
        """Главная страница должна возвращать статус 200."""
        client = Client()
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_home_page_contains_text(self):
        """Главная страница должна содержать заголовок."""
        client = Client()
        response = client.get(reverse('home'))
        assert b'Home page' in response.content


@pytest.mark.django_db
class TestLoginView:
    """Тесты страницы входа."""

    def test_login_page_returns_200(self):
        """Страница входа должна возвращать статус 200."""
        client = Client()
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_login_with_valid_credentials(self):
        """Вход с правильными данными должен перенаправлять на home."""
        # Создаём тестового пользователя
        user = User.objects.create_user(username='testuser', password='testpass123')

        client = Client()
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })

        # После успешного входа — редирект 302
        assert response.status_code == 302
        assert response.url == reverse('home')

    def test_login_with_invalid_credentials(self):
        """Вход с неправильным паролем не должен перенаправлять."""
        User.objects.create_user(username='testuser', password='testpass123')

        client = Client()
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })

        # Страница должна вернуться с формой (200), а не редирект
        assert response.status_code == 200


@pytest.mark.django_db
class TestSigninView:
    """Тесты страницы регистрации."""

    def test_signin_page_returns_200(self):
        """Страница регистрации должна возвращать статус 200."""
        client = Client()
        response = client.get(reverse('signin'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestLogoutView:
    """Тесты выхода из аккаунта."""

    def test_logout_redirects_to_home(self):
        """Выход должен перенаправлять на главную."""
        user = User.objects.create_user(username='testuser', password='testpass123')

        client = Client()
        client.login(username='testuser', password='testpass123')

        response = client.get(reverse('logout'))
        assert response.status_code == 302
        assert response.url == reverse('home')
