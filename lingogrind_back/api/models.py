from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Lesson model holds the data for each lesson that is necessary to dynamically load React components

class Lesson(models.Model):
    # Lang represented by intl. 2 character standard language code as defined here https://www.loc.gov/standards/iso639-2/php/code_list.php
    lang = models.CharField(max_length=2)

    # Priority to determine how high up on lesson list a lesson appears. Lower numbers show up higher on the list. 
    prio = models.IntegerField(default=100)

    # The name of a lesson as it is displayed on the list of lessons. 
    name = models.CharField(max_length=100, unique=True)

    # The filename of the lesson. Path not necessary
    file = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

# UserProfile class is used to associate fields with an individual user without having to create a custom user class
    
class UserProfile(models.Model):
    # User associated with this UserProfile instance. 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The lessons this user has marked as read
    lessons_read = models.ManyToManyField(Lesson)