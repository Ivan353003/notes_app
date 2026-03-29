from django.urls import path
from .views import hello_notes, notes_view, notes_list, NoteCreateView, NoteListView, NoteDetailView, NoteDeleteView, \
    NoteUpdateView

urlpatterns = [
    path('hello_notes/', hello_notes),
    path('notes_view/', notes_view),
    path('notes_list/', notes_list),
    path('', NoteListView.as_view(), name='list_notes'),
    path('create/', NoteCreateView.as_view(), name='note_create'),
    path('<int:note_id>/', NoteDetailView.as_view(), name='note_detail'),
    path('<int:note_id>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('<int:note_id>/delete/', NoteDeleteView.as_view(), name='note_delete'),
]
