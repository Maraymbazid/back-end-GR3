from django.db import models
from teatcher.models import Teacher
class Activities(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    lesson = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    contenu = models.TextField()
    

class Resource(models.Model):
    content = models.CharField(max_length=255)
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE,related_name='resources')    