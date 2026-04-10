from django.urls import path
from .views import *

urlpatterns = [
    # path('hello_notes/', hello_notes),
    # path('notes_view/', notes_view),
    # path('notes_list/', notes_list),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('', NoteListView.as_view(), name='list_notes'),
    path('create/', NoteCreateView.as_view(), name='note_create'),
    path('<int:note_id>/', NoteDetailView.as_view(), name='note_detail'),
    path('<int:note_id>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('<int:note_id>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('import/sync/', SyncBookImportView.as_view(), name='sync_import'),
    path('import/async/', AsyncBookImportView.as_view(), name='async_import'),
    path('import/comparison/', HttpClientComparisonView.as_view(), name='http_comparison'),

]
