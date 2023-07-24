from rest_framework import routers
from .views import AppleViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'apples', AppleViewSet)

urlpatterns = [
    path('', include(router.urls))
]
