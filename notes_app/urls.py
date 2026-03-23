from django.urls import path
from notes.views import hello_notes

urlpatterns = [
    path('hello_notes/', hello_notes),
]
