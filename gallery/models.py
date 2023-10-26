from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    
class Roi(models.Model):
    center_x = models.FloatField()
    center_y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

class PhotoSet(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class ParametersPhotoSet(models.Model):
    statusDetection = models.CharField(max_length=100, null = True)
    tasksId = models.CharField(max_length=200, null = True)
    countLuminaria = models.IntegerField()
    countPostacion = models.IntegerField()
    countVehiculos = models.IntegerField()
    countOtros = models.IntegerField()
    lastPhotoDetect = models.IntegerField()
    photoset = models.ForeignKey(PhotoSet, related_name='albumParamters', on_delete=models.CASCADE, null = True)
    
def user_right_image_path(instance, filename):
    return 'user_{0}/{1}/right/{2}'.format(instance.photoset.owner.id, instance.photoset,filename)

def user_left_image_path(instance, filename):
    return 'user_{0}/{1}/left/{2}'.format(instance.photoset.owner.id, instance.photoset,filename)

class Photo_pair(models.Model):
    image_r = models.FileField(upload_to=user_right_image_path)
    image_l = models.FileField(upload_to=user_left_image_path)
    photoset = models.ForeignKey(PhotoSet, related_name='album', on_delete=models.CASCADE, null = True)
    location = models.ForeignKey(Location, related_name='location_photo', on_delete=models.CASCADE, null=True)
    index = models.IntegerField(null = True)

    def get_location(self):
        return [self.location.latitude , self.location.longitude]
    def __str__(self):
        return str(self.id)
    def get_absolute_url(self):
        return reverse('gallery:index')
    
class StreetObject(models.Model):

    class ObjectType(models.TextChoices):
        POSTACION = "postacion"
        LUMINARIA = "luminaria"
        VEHICULO = "vehiculo"
        OTROS = "otros"

    name = models.CharField(max_length=50)
    photo = models.ForeignKey(Photo_pair, related_name='img', on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null = True)
    photoset = models.ForeignKey(PhotoSet, related_name='album_streetobject', on_delete=models.CASCADE, null = True)
    location = models.ForeignKey(Location, related_name='location_object', on_delete=models.CASCADE, null=True)
    roi = models.ForeignKey(Roi, related_name='roi_object', on_delete=models.CASCADE, null=True)
    objtype = models.CharField(max_length=20, choices=ObjectType.choices, null=True, default=ObjectType.OTROS)
    
    def __str__(self):
        return self.name
    
    def get_location(self):
        return [self.location.latitude , self.location.longitude]

class ObjectAttributes(models.Model):
    attribute_key = models.CharField(max_length=200)
    attribute_value = models.CharField(max_length=200)
    object = models.ForeignKey(StreetObject,related_name='attributes_object', on_delete=models.CASCADE)


