from django import forms
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'category', 'reminder']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть назву нотатки'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Введіть текст нотатки'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'reminder': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']