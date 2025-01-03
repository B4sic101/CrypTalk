
from os.path import basename
from io import BytesIO
from django.core.files.base import ContentFile
from src.models import User
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save as postSave
from django.core.files.storage import default_storage as defaultStorage


@receiver(postSave, sender=User)
def createDummyProfile(sender, instance, created, **kwargs):
    if created:
        userID = instance.userID
        
        instance.profileImage = imageGen(f"user_{userID}.jpeg")
        instance.save()

def imageGen(fileName):
    img = Image.new('RGB', (300, 300), color=(255, 255, 255))

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    return ContentFile(buffer.read(), name=fileName)

print("***signals.py loaded***")