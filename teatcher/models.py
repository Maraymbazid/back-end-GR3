from django.db import models
from django.contrib.auth.models import AbstractUser

class Teacher(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    start_date = models.DateField()
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=100,default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    

