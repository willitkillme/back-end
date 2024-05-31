from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

class Child(models.Model):
    parent = models.ForeignKey(User, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Child: {self.name}, Parent: {self.parent.username}"

class Allergy(models.Model):
    user = models.ForeignKey(User, related_name='allergies', null=True, blank=True, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, related_name='allergies', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.clean()
        super(Allergy, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return f"Allergy: {self.name} for User: {self.user.username}"
        elif self.child:
            return f"Allergy: {self.name} for Child: {self.child.name} (Parent: {self.child.parent.username})"
        return f"Allergy: {self.name} (Unassigned)"