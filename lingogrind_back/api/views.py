import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LessonSerializer
from .models import Lesson
from .forms import LoginForm

@ensure_csrf_cookie
def get_csrf(request):
    if request.method == 'GET':
        csrftoken = get_token(request)
        return JsonResponse({'csrftoken' : csrftoken}, status=status.HTTP_200_OK)
    return JsonResponse({'message':'Not a GET request'}, status=status.HTTP_401_UNAUTHORIZED)

# User/Auth Related Views
# Receive a POST request containing a username and password
# and attempts to log the user in
        
def ling_login(request):
    if request.method == 'POST':    # Ensure correct request type (POST)
        body = json.loads(request.body)
        username = body["username"].strip()
        password = body["password"].strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:    # i.e. if user was logged in
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return JsonResponse({'message':'Username and password did not match'}, status=status.HTTP_401_UNAUTHORIZED)
    return JsonResponse({'message':'Not a POST request'}, status=status.HTTP_401_UNAUTHORIZED)
        
def ling_reg(request):
    if request.method == 'POST':
        body = json.loads(request.body) #json.loads converts request body to a python dict
        username = body['username'].strip()
        password = body['password'].strip()

        user = User.objects.create_user(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
        
def ling_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'}, status=status.HTTP_200_OK)

@ensure_csrf_cookie
def get_user(request):
    return JsonResponse({'username': request.user.username})

# Database Access Views (API)

class GetLesson(APIView):
    serializer_class = LessonSerializer
    lookup_url_kwarg = 'lang'

    def get(self, request, format=None):
        lang=request.GET.get(self.lookup_url_kwarg)
        Lsns = Lesson.objects.filter(lang=lang).order_by("prio").values()
        data = LessonSerializer(Lsns, many=True).data
        return Response(data, status=status.HTTP_200_OK)