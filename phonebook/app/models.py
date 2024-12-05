from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Phonebook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phone=models.TextField()
    email=models.EmailField()
    place=models.TextField()
    whatsapp=models.TextField()
