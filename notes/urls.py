from django.urls import path
from notes.views import hello_notes, notes_view, notes_list

urlpatterns = [
    path('hello_notes/', hello_notes),
    path('notes_view/', notes_view),
    path('notes_list/', notes_list),
]
