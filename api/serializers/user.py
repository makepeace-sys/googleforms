"""User Serializer"""

# Utilities
from datetime import timedelta
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
        """Handle user and profile creation."""
        data.pop('confirmation_password')
        user = User.objects.create_user(**data, is_admin=False, is_verify=False)
        self.sending_confirmation_email(user)
        return user

    def sending_confirmation_email(self, user):
        """Send account verification link to given user."""
        verification_token = self.gen_verification_token(user)
        subject = f'Welcome ${user} verify your account to start School'
        from_email = 'Admin <noreply@forms.com>'
        html_content = render_to_string(
            'emails/user/account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, html_content, from_email, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
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


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""
    token = serializers.CharField()

    def validate(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignature:
            raise serializers.ValidationError('Verification link has expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid credentials')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Account us not active yet :(')

        self.context['payload'] = payload

    def save(self):
        """Update user's verified status."""
        
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verify = True
        user.save()
