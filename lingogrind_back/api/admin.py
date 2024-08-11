from django.contrib import admin
from .models import Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["name", "lang", "prio"]
    ordering = ["prio", "name"]
