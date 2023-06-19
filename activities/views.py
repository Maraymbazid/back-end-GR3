from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Activities,Resource
from .serializers import ActivitiesSerializer
from .serializers import ResourcesSerializer
from django.shortcuts import get_object_or_404
from teatcher.models import Teacher
teacher = Teacher.objects.get(id=1)

# class ActivitiesCreateView(APIView):
#     def post(self, request):
#         serializer = ActivitiesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


class ActivitiesCreateView(APIView):
    def post(self, request):
        name = request.data.get('name')
        subject = request.data.get('subject')
        lesson = request.data.get('lesson')
        level = request.data.get('level')
        contenu = request.data.get('contenu')
        created_by = teacher
        resources = request.data.get('resources')

        # Create the activity
        activity = Activities.objects.create(
            name=name,
            subject=subject,
            lesson=lesson,
            level=level,
            contenu=contenu,
            created_by=created_by
        )
        created_resources = []
        for resource in resources:
            content = resource['content']
            resource_obj = Resource.objects.create(
                content=content,
                activity=activity
            )
            created_resources.append(resource_obj)
        response_data = {
            'activity': {
                'id': activity.id,
                'name': activity.name,
                'subject': activity.subject,
                'lesson': activity.lesson,
                'level': activity.level,
                'contenu': activity.contenu,
                'created_by': activity.created_by.id  # Assuming 'created_by' is a ForeignKey field to the 'Teacher' model
            },
            'resources': [{
                'id': resource.id,
                'content': resource.content,
                'activity_id': resource.activity.id
            } for resource in created_resources]
        }
        return Response(response_data, status=201)
class ActivitiesListView(APIView):
    def get(self, request):
        activities = Activities.objects.all()
        serializer = ActivitiesSerializer(activities, many=True)
        return Response(serializer.data)
    
class ActivityDeteteView(APIView):
    def post(self, request, pk):
        try:
            activity = Activities.objects.get(pk=pk)
            # Delete the related resources
            activity.resources.all().delete()
            # Delete the activity
            activity.delete()
            return Response({'message': 'Activity deleted successfully.'}, status=204)
        except Activities.DoesNotExist:
            return Response({'error': 'Activity not found.'}, status=404)

class OneActivityDetailView(APIView):
    def get(self, request, pk):
        activity = get_object_or_404(Activities, id=pk)
        activity_serializer = ActivitiesSerializer(activity)
        resources = Resource.objects.filter(activity=activity)
        resource_data = []
        
        for resource in resources:
            resource_data.append({
                'resource_id': resource.id,
                'content': resource.content
            })
        
        response_data = {
            'activity': activity_serializer.data,
            'resources': resource_data
        }
        
        return Response(response_data)

class UpdateActivityView(APIView):
    def post(self, request, pk):
        try:
            activity = Activities.objects.get(id=pk)
        except Activities.DoesNotExist:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
        request.data['created_by']=1
        serializer = ActivitiesSerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()

        resources_data = request.data.get('resources')

        for resource_data in resources_data:
            resource_id = resource_data.get('resource_id')
            content = resource_data.get('content')

            try:
                if content :
                    resource = Resource.objects.get(pk=resource_id, activity=activity)
                    resource.content = content
                    resource.save()
            except Resource.DoesNotExist:
               return Response({"no": "good"}, status=200)
        return Response({"ok": "good"}, status=200)


