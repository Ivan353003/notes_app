from django.db import models
from django.urls import reverse
from django.contrib import admin


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


class ExternalBook(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=300)
    author_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']