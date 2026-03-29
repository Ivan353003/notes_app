from django.http import HttpResponse
from django.shortcuts import render
from .models import Note
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .forms import NoteForm
from datetime import timedelta
from datetime import datetime


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

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('list_notes')

class NoteListView(ListView):
    model = Note
    template_name = 'list_notes.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        category = self.request.GET.get('category')
        reminder = self.request.GET.get('reminder')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if reminder:
            queryset = queryset.filter(reminder__date=reminder)

        return queryset

class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'
    pk_url_kwarg = 'note_id'

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    context_object_name = 'note'
    pk_url_kwarg = 'note_id'
    success_url = reverse_lazy('list_notes')


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    context_object_name = 'note'
    pk_url_kwarg = 'note_id'
    success_url = reverse_lazy('list_notes')