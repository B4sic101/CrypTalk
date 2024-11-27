from django.db import models
import datetime
from django.core.validators import RegexValidator
from pygments.lexer import default


class myUser(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=20)
    profileimage = models.ImageField(upload_to="uploads/profiles", default=f'uploads/profiles/{username}.jpeg')
    created_at = models.DateField(default=datetime.date.today)
    notificationSFX = models.BooleanField(default=True)
def __str__(self):
    return self.userid