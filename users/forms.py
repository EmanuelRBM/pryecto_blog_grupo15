from django import forms
from django.contrib.auth.forms import UserCreationForm

from.models import User

# clase registro

class SignUpForm(UserCreationForm):
    class Meta:
        model = User        
        fields = ("username", "email")


# Clase inicio sesion

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class EditProfileForm(forms.Form):
    username = forms.CharField()
    about_me = forms.CharField(widget=forms.Textarea())
    image = forms.ImageField(required=False)

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def clean_username(self):
        """
        Esta función lanza una excepción si el nombre de usuario ya ha sido
        tomado por otro usuario
        """

        username = self.cleaned_data['username']
        if username != self.original_username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    'Un usuario con ese nombre ya existe.')
        return username