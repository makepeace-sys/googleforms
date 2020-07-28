"""User permission"""

# rest_framework
from rest_framework.permissions import BasePermission

# Model
from api.models import Question


class IsUserAdmin(BasePermission):
    """Admin permission"""

    def has_permission(self, request, view):
        """Allow to do actions only if the user is admin"""
        return request.user.is_admin