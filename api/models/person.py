"""Forms model"""

# Django
from django.db import models

# Models
from api.models import BaseModel, User


class Person(BaseModel):
    """Person class."""

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=200)
    user = models.ForeignKey('User',
                             on_delete=models.CASCADE,
                             related_name='get_courses'
                             )
    annotations = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
