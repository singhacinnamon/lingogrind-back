from django.db import models

# Create your models here.
class Lesson(models.Model):
    # Lang represented by intl. 2 character standard language code as defined here https://www.loc.gov/standards/iso639-2/php/code_list.php
    lang = models.CharField(max_length=2)
    # Priority to determine how high up on lesson list a lesson appears. Lower numbers show up higher on the list. 
    prio = models.IntegerField(default=100)
    # The name of a lesson as it is displayed on the list of lessons. 
    name = models.CharField(max_length=100, unique=True)
    # The filename of the lesson. Path not necessary
    file = models.CharField(max_length=50, unique=True)