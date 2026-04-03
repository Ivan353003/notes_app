from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'reminder', 'category')
    list_filter = ['category']
    search_fields = ('title', 'text')


admin.site.register(Note, NoteAdmin)