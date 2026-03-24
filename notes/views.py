from django.http import HttpResponse
from django.shortcuts import render


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