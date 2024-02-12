import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .serializers import LessonSerializer, CreateLessonSerializer
from .models import Lesson
from .forms import LoginForm


# Create your views here.
def home(request):
    return HttpResponse("Hello")

# User/Auth Related Views
# Receive a POST request containing a username and password
# and attempts to log the user in
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF Cookie Set'})
@method_decorator(ensure_csrf_cookie, name='dispatch')    
def ling_login(request):
    if request.method == 'POST':    # Ensure correct request type (POST)
        form = LoginForm(request.POST)
        if(form.isValid()): # Use Django form validation to ensure valid field entry
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:    # AKA if user was logged in
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)
            return JsonResponse({'message':'Username and password did not match'}, status.HTTP_401_UNAUTHORIZED)
        return JsonResponse({'message': 'Form Field(s) invalid'}, status=status.HTTP_401_UNAUTHORIZED)
    return JsonResponse({'message':'Not a POST request'}, status=status.HTTP_401_UNAUTHORIZED)
        
def ling_reg(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username'] #json.loads converts request body to a python dict
        password = json.loads(request.body)['password']

        print(f"Received username: {username}, password: {password}")
        print('Raw Data: "%s"' % request.body)

        user = User.objects.create_user(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
        
def ling_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'}, status=status.HTTP_200_OK)

def get_user(request):
    return JsonResponse({'username': request.user.username})
#Lesson Views
class LessonView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class GetLesson(APIView):
    serializer_class = LessonSerializer
    lookup_url_kwarg = 'lang'

    def get(self, request, format=None):
        lang=request.GET.get(self.lookup_url_kwarg)
        Lsns = Lesson.objects.filter(lang=lang).order_by("prio").values()
        data = LessonSerializer(Lsns, many=True).data
        return Response(data, status=status.HTTP_200_OK)

class CreateLessonView(APIView):
    serializer_class = CreateLessonSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            lang = serializer.data.get('lang')
            prio = serializer.data.get('prio')
            name = serializer.data.get('name')
            file = serializer.data.get('file')
            lesson = Lesson(lang=lang, prio=prio, name=name, file=file)
            lesson.save()
            return Response(LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)