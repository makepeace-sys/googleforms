"""Base model."""

# Django
from django.db import models


class BaseModel(models.Model):
    """Base model."""

    created = models.DateTimeField(
        'Created at',
        auto_now_add=True
    )
    modified = models.DateTimeField(
        'Modified at',
        auto_now=True
    )

    class Meta:
        abstract = True
