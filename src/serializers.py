from rest_framework import serializers
from src.models import User

class addContact(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["userAdded"]