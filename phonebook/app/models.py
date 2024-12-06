from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    name=models.TextField()
    email = models.EmailField(unique=True)
    password=models.TextField()
    otp = models.CharField(max_length=6)
    otp_verified = models.BooleanField(default=False)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email



class Phonebook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phone=models.TextField()
    email=models.EmailField()
    place=models.TextField()
    whatsapp=models.TextField()
