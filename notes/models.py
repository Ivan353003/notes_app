from django.db import models
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    reminder = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'note_id': self.id})