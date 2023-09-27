from django.db import models

# Create your models here.

class Map(models.Model):
    meta = models.CharField(max_length=500)