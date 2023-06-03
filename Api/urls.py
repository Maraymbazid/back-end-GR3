from django.urls import path
from Api import views

urlpatterns = [
   path('django/jsonresponsenomodel/', views.no_rest_no_model),
   path('django/jsonmodel/', views.no_rest_from_model),
]