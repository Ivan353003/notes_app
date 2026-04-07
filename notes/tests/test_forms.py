import pytest
from ..forms import NoteForm


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