from django.db import models


class Recipe(models.Model):
    name = models.CharField(blank=False, unique=True, max_length=100)
    description = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='recipes')

    class Meta:
        ordering = ('-updated',)
