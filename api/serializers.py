from rest_framework import serializers
from api.models import friendRequest
from src.models import User

class FRSerializer(serializers.ModelSerializer):
    class Meta:
        model = friendRequest
        fields = ['receiver']

class getUserIDSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)


