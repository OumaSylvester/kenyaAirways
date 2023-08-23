from rest_framework import routers
from .views import AppleViewSet
from django.urls import path, include


urlpatterns = [
    path('', include(router.urls))
]
