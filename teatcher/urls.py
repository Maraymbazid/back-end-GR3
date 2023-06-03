from django.urls import path

from .views import RegisterView,LoginView,UserView
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('teachers/register/', RegisterView.as_view()),
    path('teachers/login/', LoginView.as_view()),
    path('teachers/auth/', UserView.as_view()),
     
]