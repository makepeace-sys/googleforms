"""Form model."""

# Django
from django.db import models

# Models
from api.models import BaseModel


class Form(BaseModel):
    """Form model."""

    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
