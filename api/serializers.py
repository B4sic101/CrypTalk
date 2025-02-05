from rest_framework import serializers
from api.models import friendRequest
from uuid import uuid4

class FRSerializer(serializers.ModelSerializer):
    class Meta:
        model = friendRequest
        fields = ['receiver']

class FRreceivingSerializer(serializers.Serializer):
    requestID = serializers.UUIDField(default = uuid4)

class getUserIDSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)


