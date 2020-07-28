"""Question model."""

# Django
from django.db import models

# Models
from api.models import BaseModel, Form


class Question(BaseModel):
    """Question model."""

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
    description = models.CharField(max_length=45)
    answer = models.FloatField()

    def __str__(self):
        return f'{self.id} - {self.description}'

