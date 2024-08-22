from django.http import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import LessonSerializer
from .models import Lesson, UserProfile

@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf(request):
    if request.method == 'GET':
        csrftoken = get_token(request)
        return Response({'csrftoken' : csrftoken}, status=status.HTTP_200_OK)
    return Response({'message':'Not a GET request'}, status=status.HTTP_401_UNAUTHORIZED)


# User/Auth Related Views
# Receive a POST request containing a username and password
# and attempts to log the user in

@api_view(['POST'])        
def ling_login(request):
    if request.method == 'POST':    # Ensure correct request type (POST)
        username = request.data.get("username").strip()
        password = request.data.get("password").strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:    # i.e. if user was logged in
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'message':'Username and password did not match'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message':'Not a POST request'}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['POST'])
def ling_reg(request):
    if request.method == 'POST':
        username = request.data.get("username").strip()
        password = request.data.get("password").strip()
        user = User.objects.create_user(username=username, password=password)

        if user is not None:
            UserProfile.objects.create(user=user) #Create a UserProfile model and associate it with this user
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def ling_logout(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@ensure_csrf_cookie
def get_user(request):
    return Response({'username': request.user.username})


# Database Access Views (API)

class GetLesson(APIView):
    serializer_class = LessonSerializer
    lookup_url_kwarg = 'lang'

    def get(self, request, format=None):
        lang=request.GET.get(self.lookup_url_kwarg)
        Lsns = Lesson.objects.filter(lang=lang).order_by("prio").values()
        data = LessonSerializer(Lsns, many=True).data
        return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_read(request):
    if request.user is None or not request.user.is_authenticated:
        return Response([], status=status.HTTP_401_UNAUTHORIZED)
    user_profile = request.user.userprofile
    data = user_profile.lessons_read.all().values_list("file", flat=True)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def set_read(request):
    if request.user is None or not request.user.is_authenticated:
        return Response([], status=status.HTTP_401_UNAUTHORIZED)
    user_profile = request.user.userprofile
    file = request.data.get("file") #Specifies which lesson
    mode = request.data.get("mode") #Specifies whether it should be marked as read ("add") or unread ("remove")
    if(mode == "add"):
        user_profile.lessons_read.add(Lesson.objects.get(file=file))
    else:
        user_profile.lessons_read.remove(Lesson.objects.get(file=file))
    return Response(status=status.HTTP_200_OK)
