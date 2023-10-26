from django.urls import path

from . import views
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'gallery'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add_image/', upload_images, name='addimage'),
    path('add_set/', login_required(views.AddSetView.as_view()), name='addset'),
    path('delete_set/', delete_set, name='deleteset'),
    path('download_dxf/', download_dxf, name='downloaddxf'),
    path('images/<int:pk>/<int:pk2>/', login_required(views.ImageMapView.as_view()), name='image2'),
    path('images/old/<int:pk>/<int:pk2>/', login_required(views.ImageMapViewOld.as_view()), name='imagemapold'),
    path('images/<int:pk>/<int:pk2>/selectroi/', login_required(views.SelectROIView.as_view()), name='selectroi'),
    path('modal/<int:pk>/<int:pk2>/<int:pk3>/', login_required(views.AddAttributeView.as_view()), name='addattribute'),
    path('modal/<int:pk>/delete/', login_required(views.DeleteStreetObjectView.as_view()), name='deletestreetobject'),
    path('modal/<int:pk>/show/', login_required(views.ShowAttributeView.as_view()), name='showattributes'),
    path('images/<int:pk>/<int:pk2>/viewobjects/', login_required(views.ObjectsView.as_view()), name='viewobjects'),
    path('images/<int:pk>/<int:pk2>/detectobject/', login_required(views.DetectObjectView.as_view()), name='detectobject'),
    path('images/<int:pk>/<int:pk2>/detectobjectmanual/', login_required(views.DetectObjectViewManual.as_view()), name='detectobjectmanual'),
    
    path('zdepth/', zdepth, name='zdepth'),
    path('distanceObjects/', distanceObjects, name='distanceObjects'),
    path('objectselec/', objectselec, name='objectselec'),
    path('deleteallobjects/', deleteallobjects, name='deleteallobjects'),
    path('startdetection/', startdetection, name='startdetection'),
    path('stopdetection/', views.stopdetection, name='stopdetection'),
    path('updateprogress/', updateprogress, name='updateprogress'),
    path('updateprogressmapa/', updateprogressmapa, name='updateprogressmapa'),
    path('get_map/', get_map, name='getmap'),

    
]