"""Person serializer."""

# Django REST Framework
from rest_framework import serializers

# Model
from api.models import Person


class PersonModelSerializer(serializers.ModelSerializer):
    """Person serializer."""

    class Meta:
        """Meta class"""
        model = Person
        fields = (
            'username',
            'first_name',
            'last_name',
            'annotations'
        )
