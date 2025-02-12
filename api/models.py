from django.db import models
from uuid import uuid4
import datetime

class friendRequest(models.Model):
    requestID = models.UUIDField(primary_key=True, unique=True, default = uuid4)
    sender = models.UUIDField(max_length=20, default=uuid4)
    receiver = models.UUIDField(max_length=20, default=uuid4)

class chat(models.Model):
    chatID = models.UUIDField(primary_key=True, unique=True, default = uuid4)
    sender = models.UUIDField(default = uuid4)
    receiver = models.UUIDField(default = uuid4)
    latest_message = models.CharField(max_length=25, default="")
    crypt_key = models.CharField(max_length=255, default="101112131415161718191a1b1c1d1e1f")
    iv = models.CharField(max_length=255, default="101112131415161718191a1b1c1d1e1f")

class ChatLine(models.Model):
    messageID = models.UUIDField(primary_key=True, unique=True, default = uuid4)
    chatID = models.UUIDField(default = uuid4)
    sender = models.UUIDField(default = uuid4)
    created_at = models.DateField(default=datetime.date.today)
    content = models.TextField()