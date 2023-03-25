from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError("Password must contain at least one letter.")
        return password1

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserChangeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=150, required=True, label='Last Name')
    email = forms.EmailField(max_length=100, required=True, label='Email')

    class Meta:
        model = UserProfile
        fields = ('avatar', 'birth_date', 'email', 'first_name', 'last_name')
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
        }
