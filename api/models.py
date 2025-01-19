from django.db import models
from src.models import User
from uuid import uuid4

class friendRequest(models.Model):
    requestID = models.UUIDField(primary_key=True, unique=True, default = uuid4)
    sender = models.UUIDField(max_length=20, default = uuid4)
    receiver = models.UUIDField(max_length=20)
    state = models.BooleanField(default=False)
