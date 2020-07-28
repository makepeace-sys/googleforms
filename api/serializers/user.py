"""User Serializer"""

# Datetime
from datetime import timedelta

# JWT
import jwt

# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from api.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class"""
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email'
        )


class UserSignUpSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(
        max_length=50,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        min_length=8,
        max_length=100
    )
    confirmation_password = serializers.CharField(
        min_length=8,
        max_length=100
    )

    def validate(self, data):
        """Confirmations if the password is the same"""
        pwd = data['password']
        conf_pwd = data['confirmation_password']
        if pwd != conf_pwd:
            raise serializers.ValidationError('Password does not match')
        password_validation.validate_password(pwd)
        return data

    def create(self, data):
        data.pop('confirmation_password')
        user = User.objects.create_user(**data, is_admin=False, is_verify=False)
        self.sending_email(user)
        return user

    def sending_email(self, user):
        """Functions that sends the email verification."""
        token = self.generate_token(user)
        subject = f'Welcome ${user} verify your account to start School'
        from_email = 'Admin <noreply@forms.com>'
        content = render_to_string(
            'emails/user/email_verification.html',
            {'token': token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def generate_token(self, user):
        """Function to generate the token"""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token.decode()


class UserLoginSerializer(serializers.Serializer):
    """User login Serializer
    """
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, max_length=50)

    def validate(self, data):
        """Validate if user already exists"""

        user = authenticate(
            username=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        if not user.is_verify:
            raise serializers.ValidationError('Please verify your account to get access')
        self.context['user'] = user
        return data

    def create(self, data):
        """Get or Create a token then it's sending """
        token = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token[0].key


class UserAccountVerificationSerializer(serializers.Serializer):
    """User Account verification by token
    """
    token = serializers.CharField()

    def validate_token(self, data):
        """Validate token
        here we validate that the token is correct and it is valid
        """
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignature:
            raise serializers.ValidationError('verification link has expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid Token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid Token')

        self.context['payload'] = payload

    def save(self):
        """Update the verification status in user"""
        
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verify = True
        user.save()
