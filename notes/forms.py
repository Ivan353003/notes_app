from django import forms
from .models import Note

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
