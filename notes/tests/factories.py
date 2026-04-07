import factory
from datetime import datetime
from ..models import Category, Note

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker('word')

class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Faker('sentence', nb_words=4)
    text = factory.Faker('sentence', nb_words=50)
    category = factory.SubFactory(CategoryFactory)
    reminder = factory.LazyFunction(datetime.now)