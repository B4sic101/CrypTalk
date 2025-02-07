from django.db import models
from src.models import User
from uuid import uuid4

class friendRequest(models.Model):
    requestID = models.UUIDField(primary_key=True, unique=True, default = uuid4)
    sender = models.UUIDField(max_length=20, default=uuid4)
    receiver = models.UUIDField(max_length=20, default=uuid4)

class chat(models.Model):
    chatID = models.UUIDField(primary_key=True, unique=True, default = uuid4)
    sender = models.UUIDField(unique=True, default = uuid4)
    receiver = models.UUIDField(unique=True, default = uuid4)
    crypt_key = models.CharField(unique=True, max_length=255, default="101112131415161718191a1b1c1d1e1f")
    iv = models.CharField(unique=True, max_length=255, default="101112131415161718191a1b1c1d1e1f")