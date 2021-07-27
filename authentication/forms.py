from django import forms
from appuser.models import UserModel
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = [
            'username',
            'password1',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off'}), max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
