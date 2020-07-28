"""User view set."""

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Serializer
from api.serializers import (UserSignUpSerializer,
                             UserModelSerializer,
                             UserLoginSerializer,
                             UserAccountVerificationSerializer
                             )


class UserViewSet(viewsets.GenericViewSet):
    """User view sets."""

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permissions = []
        if self.action in ['signup', 'login', 'verification']:
            permissions.append(AllowAny)
        return [permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """signup functions
        """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login allow user to gain access into the system."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def verification(self, request):
        """Handle the request of email verification."""
        serializer = UserAccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": "Congratulations your account is verified, please login"
        }
        return Response(data=data, status=status.HTTP_200_OK)