# Django
from django.urls import path, include
from django.conf.urls import url

# Django REST Framework
from rest_framework.routers import DefaultRouter

# View sets
from .viewsets import UserViewSet

from api import viewsets

router = DefaultRouter()
router.register(r'users', viewset=UserViewSet, basename='user')

urlpatterns = [
    path('api/v1/', include(router.urls)),

]