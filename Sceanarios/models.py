from teatcher.models import Teacher
from django.db import models

class Scenario(models.Model):
    etablissement = models.CharField(max_length=100)
    unite = models.CharField(max_length=50)
    niveau = models.CharField(max_length=50)
    lesson = models.CharField(max_length=100)
    duree = models.PositiveIntegerField()  # Duration in minutes
    methode_de_travail = models.CharField(max_length=20)
    situation = models.TextField()
    competence = models.TextField()
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    
class Objectifs(models.Model):
    contenu = models.TextField()
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE,related_name='objectifs')
    
class ScenarioActivity(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='Scenario')
    objectif = models.CharField(max_length=100)
    duree = models.CharField(max_length=100)
    support = models.CharField(max_length=100)
    activityapprenant = models.TextField()
    activityenseignant = models.TextField()
class ImageScenario(models.Model):
    contenu = models.CharField(max_length=255)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE,related_name='Scenarioimages')

