from django.test import TestCase
from django.urls import reverse

from ..models import User
from ..forms import SignUpForm


class TestSignUpView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )
        self.data = {
            'username': 'test',
            'email': 'test@hotmail.com',
            'password1': 'test12345',
            'password2': 'test12345'
        }

    def test_signup_returns_200(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)

        # Verifique que usamos la plantilla correcta

        self.assertTemplateUsed(response, 'users/signup.html')

    def test_user_is_logged_in(self):
        response = self.client.post(
            reverse('users:signup'), self.data, follow=True
        )
        user = response.context.get('user')

        self.assertTrue(user.is_authenticated)

    def test_new_user_is_registered(self):

        # Podemos comprobar que un usuario se ha registrado intentando encontrarlo
        # en la base de datos pero prefiero el método con count ()

        nb_old_users = User.objects.count()  # llamando a count para encontrar antes a los usuarios
        self.client.post(reverse('users:signup'), self.data)
        nb_new_users = User.objects.count()  # llamando a count para encontrar despues a los usuarios
        
        # asegurarse de que se haya agregado 1 usuario
        self.assertEqual(nb_new_users, nb_old_users + 1)

    def test_redirect_if_user_is_authenticated(self):

        # Si el usuario está autenticado e intenta acceder
        # la página de registro, se le redirige a la página de inicio
        login = self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.get(reverse('users:signup'))

        self.assertRedirects(response, reverse('nucleo:home'))

    def test_invalid_form(self):

        # No damos un nombre de usuario
        
        response = self.client.post(reverse('users:signup'), {
            "email": "test@admin.com",
            "password1": "test12345",
            "password2": "test12345",
        })
        form = response.context.get('form')

        self.assertFalse(form.is_valid())