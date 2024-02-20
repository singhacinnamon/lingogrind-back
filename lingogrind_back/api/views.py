from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework import status

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