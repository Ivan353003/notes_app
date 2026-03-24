from django.urls import path
from notes.views import hello_notes, notes_view

urlpatterns = [
    path('hello_notes/', hello_notes),
    path('notes_view/', notes_view),
]
