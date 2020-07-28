"""Users model."""

# Django
from django.db import models

# Models
from django.contrib.auth.models import AbstractUser
from api.models.base import BaseModel


class User(AbstractUser, BaseModel):
    """User model."""

    email = models.CharField(max_length=50,
                             unique=True,
                             error_messages={
                                 'unique': 'A user with that email already exists.'
                                }
                             )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_admin = models.BooleanField(default=False)
    is_verify = models.BooleanField(
        default=False,
        help_text='Set to true when the user have verified its email address'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

