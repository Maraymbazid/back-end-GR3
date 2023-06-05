from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import Teacher
import jwt, datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import dotenv
import os,openai
from django.http import JsonResponse
dotenv.load_dotenv()
#api_key = os.getenv('OPENAI_KEY')
from django.views.decorators.csrf import csrf_exempt



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class LoginView(APIView):
     def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Teacher.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True,samesite='None')
        response.data = {
            'jwt': token
        }
        return response
class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed('Invalid token!')

        user = Teacher.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
@csrf_exempt
# def chatactivities(request):
#     if api_key is not None :
#         openai.api_key = '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'
#         subject="math"
#         lesson_name="equation"
#         prompt = f"matiere: {subject}\n la lecon : {lesson_name}\n propose moi une activité:"
#         response = openai.Completion.create(
#             engine='text-davinci-003', 
#             prompt=prompt,
#             max_tokens=100,  
#            ) 
#         activity_details = response.choices[0].text.strip()
#         return activity_details
    
def chatactivities(request):
    if request.method == 'GET':
        api_key = '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'  # Replace with your actual OpenAI API key
        openai.api_key = api_key
        subject = "math"
        lesson_name = "equation"
        prompt = f"translate me this: {subject} on spanish\n"
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=40,
            temperature=0.5,
        )

        if 'error' in response:
            print(response['error'])  # Print the error response from the OpenAI API

        activity_details = response.choices[0].text.strip()

        return JsonResponse({'activity_details': activity_details})

    return JsonResponse({'error': 'Invalid request method'})

# Rm11a}72RLK; mryamroot taamehoj_mryamroot  taamehoj_scenario


    
       