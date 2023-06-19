from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Scenario,Objectifs
from .models import ScenarioActivity
from .serializers import ScenarioActivitySerializer,ImageScenarioSerializer,ScenarioSerializer,ObjectifsSerializer
import logging
from teatcher.models import Teacher
from django.shortcuts import get_object_or_404
teacher = Teacher.objects.get(id=1)

logger = logging.getLogger(__name__)

class CreateScenarioFirstAPIView(APIView):
    def post(self, request):
        etablissement = request.data.get('etablissement')
        unite = request.data.get('unite')
        niveau = request.data.get('niveau')
        lesson = request.data.get('lesson')
        duree = request.data.get('duree')
        methode_de_travail = request.data.get('methode_de_travail')
        
        try:
            # Perform validation on the data if necessary
            
            scenario = Scenario(
                etablissement=etablissement,
                unite=unite,
                niveau=niveau,
                lesson=lesson,
                duree=duree,
                methode_de_travail=methode_de_travail,
                created_by=teacher
            )
            scenario.save()
            
            if scenario.id:
                response = {
                    'status': 'OK',
                    'message': 'Scenario created successfully.',
                    'scenario_id': scenario.id,
                }
            else:
                response = {
                    'status': 'ERROR',
                    'message': 'Failed to create scenario.',
                }
            
            return Response(response)
        
        except Exception as e:
            logger.error(f'Error creating scenario: {str(e)}')
            response = {
                'status': 'ERROR',
                'message': 'Failed to create scenario.',
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateScenarioSecondAPIView(APIView):
    def post(self, request, format=None):
        scenario_id = request.data.get('scenario_id')
        competence_value = request.data.get('competence')
        situation_value = request.data.get('situation')
        objectifs = request.data.get('objectifs')

        try:
            # Get the existing Scenario record
            scenario = Scenario.objects.get(id=scenario_id)
                
                # Update the competence and situation fields
            scenario.competence = competence_value
            scenario.situation = situation_value
            scenario.save()

            # Create or update the objectif records
            for objectif_value in objectifs:
                content = objectif_value['content']
                Objectifs.objects.create(contenu=content, scenario=scenario)
            
            return Response({'status': 'OK', 'message': 'Competence and related data updated successfully.'})

        except Scenario.DoesNotExist:
            return Response({'status': 'Error', 'message': 'Scenario not found.'})
        
class CreateScenarioThirdAPIView(APIView):
       def post(self, request):
        scenario_id = request.data.get('scenarioId')
        form_datas = request.data.get('formDatas')
        
        if scenario_id is None:
            return Response({'message': 'scenarioId is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        for form_data in form_datas:
            form_data['scenario_id'] = scenario_id
            serializer = ScenarioActivitySerializer(data=form_data)
            if serializer.is_valid():
               serializer.save(scenario_id=scenario_id)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Scenario activities created successfully'})
    
class ScenarioDataAPIView(APIView):
    def get(self, request,pk):
        scenario = get_object_or_404(Scenario, id=pk)
        objectives = scenario.objectifs.all()
        activities = scenario.Scenario.all()

        # Prepare the data to be returned
        scenario_data = {
            'id': scenario.id,
            'etablissement': scenario.etablissement,
            'unite': scenario.unite,
            'niveau': scenario.niveau,
            'lesson': scenario.lesson,
            'duree': scenario.duree,
            'methode_de_travail': scenario.methode_de_travail,
            'situation': scenario.situation,
            'competence': scenario.competence,
            'created_by': scenario.created_by.name,
            'objectifs': [{'contenu': obj.contenu} for obj in objectives],
            'activities': [
                {
                    'objectif': activity.objectif,
                    'duree': activity.duree,
                    'support': activity.support,
                    'activityapprenant': activity.activityapprenant,
                    'activityenseignant': activity.activityenseignant
                }
                for activity in activities
            ],
        }

        return Response(scenario_data)
class ImageScenarioCreateAPIView(APIView):
    def post(self, request, format=None):
        scenario_id = request.data.get('scenarioId')
        serializer = ImageScenarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(scenario_id=scenario_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
class ScenarioListAPIView(APIView):
    def get(self, request):
        scenarios = Scenario.objects.all()
        serializer = ScenarioSerializer(scenarios, many=True)
        return Response(serializer.data)
    
class ScenarioDeleteAPIView(APIView):
    def post(self, request, pk):
        try:
            scenario = Scenario.objects.get(id=pk)
            activities = ScenarioActivity.objects.filter(scenario=scenario)
            objectives = Objectifs.objects.filter(scenario=scenario)
            activities.delete()
            objectives.delete()
            scenario.delete()
            return Response({'message': 'Scenario deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Scenario.DoesNotExist:
            return Response({'error': 'Scenario does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ScenarioFirstOneEditAPIView(APIView):
   def get(self, request, pk):
        try:
            scenario = Scenario.objects.get(id=pk)
            objectives = scenario.objectifs.all()
            activities = scenario.Scenario.all()
            
            scenario_serializer = ScenarioSerializer(scenario)
            objectives_serializer = ObjectifsSerializer(objectives, many=True)
            activities_serializer = ScenarioActivitySerializer(activities, many=True)

            return Response({
                'scenario': scenario_serializer.data,
                'objectives': objectives_serializer.data,
                'activities': activities_serializer.data
            }, status=status.HTTP_200_OK)

        except Scenario.DoesNotExist:
            return Response({'error': 'Scenario does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class ScenarioUpdateFirstPartAPIView(APIView):
    def post(self, request):
        scenario_name = request.data.get('scenario_name')
        first_part_data = {
            'unite': request.data.get('unite'),
            'lesson': request.data.get('lesson'),
            'etablissement': request.data.get('etablissement'),
            'duree': request.data.get('duree'),
            'methode_de_travail': request.data.get('methode_de_travail'),
            'niveau': request.data.get('niveau'),
        }
        try:
            scenario = Scenario.objects.get(id=scenario_name)
            serializer = ScenarioSerializer(scenario, data=first_part_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Scenario.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=404)
        
class UpdateSecondPartAPIView(APIView):
    def post(self, request):
        try:
            competence = request.data.get('competence')
            situation = request.data.get('situation')
            objectifs_data = request.data.get('objectifs')
            scenario_id = 28
            scenario = Scenario.objects.get(id=scenario_id)
            scenario.competence = competence
            scenario.situation = situation
            scenario.save()
            for objectif_value in objectifs_data:
                objectif_id = objectif_value['id']
                content = objectif_value['contenu']
                obj = Objectifs.objects.get(id=objectif_id, scenario=scenario)
                obj.contenu = content
                obj.save()

                
            
            return Response({'status': 'OK', 'message': 'Competence and related data updated successfully.'})

        except Scenario.DoesNotExist:
            return Response({'error': 'Scenario does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UpdateThirdPart(APIView):
    def post(self, request):
        try:
            scenario_id = request.data.get('scenarioId')
            form_datas = request.data.get('formDatas')

            for form_data in form_datas:
                activity_id = form_data.get('id')  # Assuming each activity has an ID field
                objectif = form_data.get('objectif')
                duree = form_data.get('duree')
                support = form_data.get('support')
                activityapprenant = form_data.get('activityapprenant')
                activityenseignant = form_data.get('activityenseignant')

                if activity_id:
                    activity = ScenarioActivity.objects.get(id=activity_id, scenario_id=scenario_id)
                    activity.objectif = objectif
                    activity.duree = duree
                    activity.support = support
                    activity.activityapprenant = activityapprenant
                    activity.activityenseignant = activityenseignant
                    activity.save()
                else:
                    activity = ScenarioActivity.objects.create(
                        objectif=objectif,
                        duree=duree,
                        support=support,
                        activityapprenant=activityapprenant,
                        activityenseignant=activityenseignant,
                        scenario_id=scenario_id
                    )

            return Response({'status': 'OK', 'message': 'Activities updated successfully.'})

        except ScenarioActivity.DoesNotExist:
            return Response({'error': 'Activity does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


 




    
                
                

