"""
URL configuration for lingogrind_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import home, LessonView, GetLesson, ling_login, ling_reg, get_user, ling_logout
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home),
    path('lsn', LessonView.as_view()),
    path('get-lsn', GetLesson.as_view()),
    path('ling_login/', ling_login, name="ling_login"),
    path('ling_reg/', ling_reg, name="ling_reg"),
    path('get_user/', get_user, name="get_user"),
    path('ling_logout', ling_logout, name="ling_logout")
]