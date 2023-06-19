from rest_framework import serializers
from .models import ScenarioActivity,ImageScenario,Scenario,Objectifs

class ScenarioActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioActivity
        fields = ['id','objectif', 'duree', 'support', 'activityapprenant', 'activityenseignant','scenario_id']
class ImageScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageScenario
        fields = ('id', 'contenu', 'scenario_id')
        
class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ('id', 'etablissement', 'unite', 'niveau', 'lesson', 'duree', 'methode_de_travail', 'competence', 'situation')
class ObjectifsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectifs
        fields = ['id', 'contenu', 'scenario_id']
