import uuid, datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have email address.")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

class User(AbstractBaseUser):
    userID = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False, unique=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    password = models.CharField(max_length=88) # 20 in user input
    profileImage = models.ImageField(upload_to="profiles/", default="default.jpg")
    created_at = models.DateField(default=datetime.date.today)
    notificationSFX = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return False
    
    def has_module_perms(self, app_label):
        return False
    
    @property
    def is_staff(self):
        return self.is_admin
