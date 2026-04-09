import pytest
from ..forms import NoteForm
from ..models import Note

@pytest.mark.django_db
def test_note_form_create(category):
    form_data = {
        'title': 'Біг',
        'text': 'Пробігти 10(+3) км',
        'category': category.id,
        'reminder': '2026-04-04 04:00:33',
    }

    form = NoteForm(data=form_data)

    assert form.is_valid()
    note = form.save()

    assert Note.objects.count() == 1
    assert note.title == 'Біг'


@pytest.mark.django_db
def test_note_form_update(note, category):
    form_data = {
        'title': 'Оновлений біг',
        'text': 'Пробігти 15 км',
        'category': category.id,
        'reminder': '2026-04-05 05:00:00',
    }

    form = NoteForm(data=form_data, instance=note)

    assert form.is_valid()
    updated_note = form.save()

    assert updated_note.id == note.id
    assert updated_note.title == 'Оновлений біг'
    assert updated_note.text == 'Пробігти 15 км'


@pytest.mark.django_db
def test_note_form_valid(category):
    form_data = {
        'title': 'Біг',
        'text': 'Пробігти 10(+3) км',
        'category': category.id,
        'reminder': '2026-04-04 04:00:33',
    }

    form = NoteForm(data=form_data)
    print(form.errors)
    assert form.is_valid()


@pytest.mark.django_db
def test_note_form_empty_title(category):
    form_data = {
        'title': '',
        'text': 'Пробігти 10(+3) км',
        'category': category.id,
        'reminder': '2026-04-04 04:00:33',
    }

    form = NoteForm(data=form_data)
    assert not form.is_valid()
    assert 'title' in form.errors


@pytest.mark.django_db
def test_note_form_empty_text(category):
    form_data = {
        'title': 'Біг',
        'text': '',
        'category': category.id,
        'reminder': '2026-04-04 04:00:33',
    }

    form = NoteForm(data=form_data)
    assert not form.is_valid()
    assert 'text' in form.errors