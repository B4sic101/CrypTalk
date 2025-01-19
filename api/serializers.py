from rest_framework import serializers
from api.models import friendRequest

class FRSerializer(serializers.ModelSerializer):
    class Meta:
        model = friendRequest
        fields = ['receiver']