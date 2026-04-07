import pytest

from django.db.models import Count

from .factories import NoteFactory, CategoryFactory
from ..models import Note, Category


@pytest.mark.django_db
def test_note_creation():
    category = Category.objects.create(title='Home')

    note = Note.objects.create(
        title='Біг',
        text='Пробігти 10(+3) км',
        reminder='2026-04-04 04:00:33',
        category=category,
    )
    assert note.id is not None
    assert str(note) == 'Біг'


@pytest.mark.django_db
def test_note_str(note):
    note.title = 'Тестова нотатка'
    note.save()

    assert str(note) == 'Тестова нотатка'


@pytest.mark.django_db
def test_note_cascade_delete(category):
    Note.objects.create(
        title='Нотатка 1', text='Текст 1', category=category, reminder='2026-04-07 10:00:00'
    )
    Note.objects.create(
        title='Нотатка 2', text='Текст 2', category=category, reminder='2026-04-06 10:00:00'
    )
    category_id = category.id
    assert Note.objects.filter(category_id=category_id).count() == 2

    category.delete()
    assert Note.objects.filter(category_id=category_id).count() == 0


@pytest.mark.django_db
def test_category_notes_count():
    category = CategoryFactory()
    NoteFactory.create_batch(3, category=category)

    result = Category.objects.annotate(
        notes_count=Count('notes')
    ).get(id=category.id)
    assert result.notes_count == 3