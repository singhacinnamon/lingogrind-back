from django.apps import AppConfig

# allows us to tell Django that the lingogrind_back app is installed in settings.py
class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lingogrind_back'
