from django.urls import path
from .views import map

app_name = 'maps'
urlpatterns = [
    path('map/', map, name='map'),

]