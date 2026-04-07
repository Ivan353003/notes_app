import pytest
from .factories import NoteFactory, CategoryFactory

@pytest.fixture
def category():
    return CategoryFactory()

@pytest.fixture
def note(category):
    return NoteFactory(category=category)