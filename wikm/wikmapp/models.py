from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db.models.signals import post_save


class Allergy(models.Model):
    user = models.ForeignKey(User,related_name='allergies', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Field to store the name of the allergy

    def __str__(self):
        return f"Allergy: {self.name} for User: {self.user.username}"

