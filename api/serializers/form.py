"""Form serializer."""

# Django REST Framework
from rest_framework import serializers

# Model
from api.models import Form, Person


class FormModelSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(read_only=True, source='user')


