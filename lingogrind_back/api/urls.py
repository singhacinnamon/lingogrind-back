from django.urls import path
from .views import *

urlpatterns = [
    path('ling_login/', ling_login, name="ling_login"),
    path('ling_reg/', ling_reg, name="ling_reg"),
    path('get_user/', get_user, name="get_user"),
    path('ling_logout/', ling_logout, name="ling_logout"),
    path('get_csrf/', get_csrf, name="get_csrf"),
    path('get-lsn/', GetLesson.as_view()),
    path('get_read/', get_read, name="get_read"),
    path('set_read/', set_read, name="set_read"),
]