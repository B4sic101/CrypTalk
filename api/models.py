from django.db import models
from src.models import User

class friendRequest(models.Model):
    requestID = models.UUIDField(primary_key=True, unique=True, default=1)
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    state = models.BooleanField(default=False)
