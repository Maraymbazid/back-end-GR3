from rest_framework import serializers
from .models import Activities, Resource

class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['content', 'activity']

class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ['id', 'name', 'subject', 'lesson', 'level', 'created_at', 'created_by', 'contenu',]

    def create(self, validated_data):
        resources_data = validated_data.pop('resources')
        activities = Activities.objects.create(**validated_data)
        for resource_data in resources_data:
            Resource.objects.create(activity=activities, **resource_data)
        return activities
