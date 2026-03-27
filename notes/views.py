from django.http import HttpResponse
from django.shortcuts import render
from .models import Note


def hello_notes(request):
    return HttpResponse("Hello from Notes app.")

def notes_view(request):
    notes = [
        {
            'title': 'Купити продукти',
            'items': ['Молоко', 'Хліб', 'Яйця', 'Смаколики']
        },
        {
            'title': 'Навчання',
            'items': ['Зробити завдання по темі: HTML, CSS', 'Зробити завдання по темі: Мультипроцесорність']
        },
        {
            'title': 'Спорт',
            'items': ['Зробити ранкову пробіжку', 'Відвезти доньку на акробатику']
        },
    ]
    return render(request, 'index.html', {'notes': notes})

def notes_list(request):
    notes = Note.objects.all()
    return render(request, 'notes_list.html', {'notes': notes})