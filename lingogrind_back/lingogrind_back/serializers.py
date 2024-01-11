from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'lang', 'prio', 'name', 'file')

class CreateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('lang', 'prio', 'name', 'file')