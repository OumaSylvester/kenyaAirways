from rest_framework import viewsets
from ..models import Apple
from .serializers import AppleModelSerializer


class AppleViewSet(viewsets.ModelViewSet):
    queryset = Apple.objects.all()
    serializer_class = AppleModelSerializer
