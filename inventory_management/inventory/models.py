# models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Make name unique
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
