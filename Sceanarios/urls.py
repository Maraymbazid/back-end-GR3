from .views import CreateScenarioFirstAPIView,CreateScenarioSecondAPIView,CreateScenarioThirdAPIView,ScenarioDataAPIView,ImageScenarioCreateAPIView,ScenarioListAPIView,ScenarioDeleteAPIView,ScenarioFirstOneEditAPIView,ScenarioUpdateFirstPartAPIView,UpdateSecondPartAPIView,UpdateThirdPart
from django.urls import path

urlpatterns = [
    path('createfirstpart/', CreateScenarioFirstAPIView.as_view(), name='first-create'),
    path('createsecondpart/', CreateScenarioSecondAPIView.as_view(), name='second-create'),
    path('createthirdpart/', CreateScenarioThirdAPIView.as_view(), name='third-create'),
    path('getonescenario/<int:pk>/', ScenarioDataAPIView.as_view(), name='scenario-data'),
    path('storeimagescenario/', ImageScenarioCreateAPIView.as_view(), name='scenario-store'),
    path('getallsceanrio/', ScenarioListAPIView.as_view(), name='scenario-all'),
    path('deletescenario/<int:pk>/', ScenarioDeleteAPIView.as_view(), name='scenario-delete'),
    path('editfirstpart/<int:pk>/', ScenarioFirstOneEditAPIView.as_view(), name='scenario-editone'),
    path('updatefirstpart/', ScenarioUpdateFirstPartAPIView.as_view(), name='scenario-updateone'),
    path('updatesecondpart/', UpdateSecondPartAPIView.as_view(), name='scenario-updatetwo'),
    path('updatethirdpart/', UpdateThirdPart.as_view(), name='scenario-updatethree'),

  
]