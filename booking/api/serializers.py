from rest_framework import serializers
from .. models import Apple

class AppleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apple
        fields = ('id', 'year_of_production', 'breed', 'row', 'column', 'geolocation')