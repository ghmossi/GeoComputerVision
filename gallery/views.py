# Create your views here.
import json
import logging

from django.http import JsonResponse
from django.template import Template
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from GPSPhoto import gpsphoto
import cv2
from yolov.mydetect import detect
from .models import *
from .forms import PhotoForm, SetForm, DeleteForm, AddObjectForm, ObjectAttributeForm
from .utils import *
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalReadView
from django.shortcuts import render
import os
import geopandas as gpd
from yolov.models.experimental import attempt_load
from yolov.utils.torch_utils import select_device
from django.core import serializers

from multiprocessing import Process
import time
from .tasks import mitarea
from celery.result import AsyncResult
from celery.app import default_app
from celery import current_app

def canvas_view(request):
    return render(request, 'gallery/canvas.html')

def canvas_view(request):
    return render(request, 'gallery/canvas.html')

class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    context_object_name = 'image_sets_list'
    ordering = ['-id']
    def get_queryset(self):
        return PhotoSet.objects.order_by('id').reverse()

class ImageMapView(generic.ListView):
    model = Photo_pair
    template_name = 'gallery/image_map.html'
    context_object_name = 'photopair'

    def get_context_data(self, **kwargs):
        context = super(ImageMapView, self).get_context_data(**kwargs)
        ps = PhotoSet.objects.get(id = self.kwargs['pk'])
        context['location'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']).location
        context['location_next'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']+10).location
        data_list = []
        data_list2 = []
        
        for obj2 in Photo_pair.objects.filter(photoset = ps).all():
            data_dict = {
                    'latitude': obj2.location.latitude,
                    'longitude': obj2.location.longitude,
                    'index': obj2.index,
                    'tipo': "photo",
                    'url': obj2.image_r.url
                }
            data_list.append(data_dict)
        context['data'] = json.dumps(data_list) 

        for object2 in StreetObject.objects.filter(photoset = PhotoSet.objects.get(id=self.kwargs['pk'])).all():
                data_dict2 = {
                    'latitude': object2.location.latitude,
                    'longitude': object2.location.longitude,
                    'index': object2.photo.index,
                    'tipo': object2.objtype
                }
                data_list2.append(data_dict2)
        context['data2'] = json.dumps(data_list2)

        data_list3 = []
        data_dict3 = {
                    'latitude': context['location'].latitude,
                    'longitude': context['location'].longitude,
                    'dataset': self.kwargs['pk'],
                    'photoindex': self.kwargs['pk2'],
                }
        data_list3.append(data_dict3)
        context['data3'] = json.dumps(data_list3)

        index=self.kwargs['pk2']
        location=Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']).location
        location_next = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=index+10).location
        azimuthCurrent=Azimuth(location.latitude,location.longitude,location_next.latitude,location_next.longitude)
        location_next10 = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=index+20).location
        azimuthNext10=Azimuth(location_next.latitude,location_next.longitude,location_next10.latitude,location_next10.longitude)
        if abs(azimuthCurrent - azimuthNext10) <= 3:
            context['location_next']=location_next = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=index+10).location    
            print("DIF AZIMUTH: ",str(abs(azimuthCurrent - azimuthNext10)))
        else:
            print("DIF AZIMUTH: ",str(abs(azimuthCurrent - azimuthNext10)))
            context['location_next']=location_next = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=index+2).location
        data_list4 = []
        data_dict4 = {
                    'latitude': context['location_next'].latitude,
                    'longitude': context['location_next'].longitude,
                    'dataset': self.kwargs['pk'],

                    'photoindex': self.kwargs['pk2'],
                }
        data_list4.append(data_dict4)
        context['data4'] = json.dumps(data_list4)
        return context
    def get_queryset(self):
        return Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2'])

class ImageMapViewOld(generic.ListView):
    model = Photo_pair
    template_name = 'gallery/image_map_old.html'
    context_object_name = 'photopair'

    def get_context_data(self, **kwargs):
        context = super(ImageMapViewOld, self).get_context_data(**kwargs)
        ps = PhotoSet.objects.get(id = self.kwargs['pk'])
        context['next'] = min(self.kwargs['pk2']+1,Photo_pair.objects.filter(photoset = ps).latest('index').index)
        context['previous'] = max(self.kwargs['pk2']-1,0)
        context['location'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']).location    
        return context
    def get_queryset(self):
        return Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2'])


class AddSetView(generic.FormView):
    model = PhotoSet
    form_class = SetForm
    template_name = 'gallery/add_set.html'
    def get_success_url(self):
        return reverse("gallery:index")
    def form_valid(self, form):
        form.save()
        return super(AddSetView, self).form_valid(form)
    def get_queryset(self):
        return PhotoSet.objects.all()

@login_required(login_url='/users/login/')
def delete_set(request):
    if request.method == 'POST':
        form = DeleteForm(request.POST,user=request.user)
        if form.is_valid():
            instance = form.cleaned_data.get('title')
            instance.delete()
            return HttpResponseRedirect(reverse('gallery:index'))
    else:
        form = DeleteForm(user=request.user)
    return render(request, 'gallery/delete_set.html',{'form': form})

def upload_images(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            images_r = request.FILES.getlist('image_r')
            images_l = request.FILES.getlist('image_l')
            images = zip(images_r, images_l)
            ps = form.cleaned_data['photoset']
            try:
                ind = Photo_pair.objects.filter(photoset = ps).latest('index').index + 1
            except:
                ind = 0
                ParametersPhotoSet.objects.create(photoset=ps, countLuminaria=0,countPostacion=0,countVehiculos=0,countOtros=0,lastPhotoDetect=0)
            for img in images:
                Photo_pair.objects.create(image_r = img[0], image_l = img[1], photoset=ps, index = ind)
                currentphotopair = ps.album.get(index=ind) 
                folder = 'media/ ' #para linux
                #folder = 'media\' #para windows
                imageurl = folder[:len(folder)-1] + str(currentphotopair.image_r)
                try:
                    loc = Location.objects.create(latitude = gpsphoto.getGPSData(imageurl)["Latitude"],longitude = gpsphoto.getGPSData(imageurl)["Longitude"])               
                    print("ubicacion",loc)
                    currentphotopair.location = loc                  
                    currentphotopair.save()
                except:
                    pass
                ind += 1
            return HttpResponseRedirect(reverse('gallery:index'))
    else:
        form = PhotoForm(user=request.user)
    return render(request, 'gallery/add_image.html',{'form': form})

def download_dxf(request):
    if request.method == 'POST':
        form = DeleteForm(request.POST,user=request.user)
        if form.is_valid():
            ps = form.cleaned_data.get('title')
            filename = ps.title + '.dxf'
            fl_path = 'media/temp/' + filename # media\
            generate_DXF(fl_path,ps)
            fl = open(fl_path, 'r')
            response = HttpResponse(fl)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            if os.path.isfile(fl_path):
                os.remove(fl_path)
            return response
    else:
        form = DeleteForm(user=request.user)
    return render(request, 'gallery/export_dxf.html',{'form': form})
    
class SelectROIView(generic.FormView):
    model = Photo_pair
    template_name = 'gallery/selectroi.html'
    context_object_name = 'photopair'
    form_class = AddObjectForm

    def get_context_data(self, **kwargs):
        context = super(SelectROIView, self).get_context_data(**kwargs)
        ps = PhotoSet.objects.get(id = self.kwargs['pk'])
        context['photopair'] = Photo_pair.objects.filter(photoset = ps).get(index=self.kwargs['pk2'])
        context['next'] = min(self.kwargs['pk2']+1,Photo_pair.objects.filter(photoset = ps).latest('index').index)
        context['previous'] = max(self.kwargs['pk2']-1,0)
        context['location'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']).location
        if self.kwargs['pk2']==0:
            context['location_next'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']).location
        else:
            context['location_next'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']+10).location
        
        return context
    def form_valid(self, form):
        name = form.cleaned_data['object']['name']
        description = form.cleaned_data['object']['description']
        objtype = form.cleaned_data['object']['objtype']
        lat = form.cleaned_data['loc']['latitude']
        lon = form.cleaned_data['loc']['longitude']
        loc = Location.objects.create(latitude = lat,longitude = lon)
        roi_x = form.cleaned_data['roi']['center_x']
        roi_y = form.cleaned_data['roi']['center_y']
        roi_w = form.cleaned_data['roi']['width']
        roi_h = form.cleaned_data['roi']['height']
        roi = Roi.objects.create(center_x = roi_x,center_y = roi_y,width = roi_w,height = roi_h)
        photo = Photo_pair.objects.filter(photoset = self.kwargs['pk']).get(index=self.kwargs['pk2'])
        ps = PhotoSet.objects.get(id = self.kwargs['pk'])
        StreetObject.objects.create(name = name, photo = photo,photoset =ps, description = description, location = loc, roi = roi, objtype = objtype)
        return super(SelectROIView, self).form_valid(form)
    def get_queryset(self):     
        return Photo_pair.objects.filter(photoset = [PhotoSet.objects.get(id = self.kwargs['pk'])]).get(index=self.kwargs['pk2'])
    def get_success_url(self):
        return reverse("gallery:selectroi", kwargs={'pk': self.kwargs['pk'],'pk2': self.kwargs['pk2']})
    
class ShowAttributeView(BSModalReadView):
    model = StreetObject
    template_name = 'gallery/modals/show_attributes.html' 

class AddAttributeView(BSModalCreateView):
    template_name = 'gallery/modals/add_attribute.html'
    form_class = ObjectAttributeForm
    success_message = 'Success: Se guardo el atributo.'
    def form_valid(self, form):
        streetobject = StreetObject.objects.get(id = self.kwargs['pk3'])
        form.instance.object = streetobject
        return super(AddAttributeView, self).form_valid(form)
    def get_success_url(self):
        return reverse("gallery:selectroi", kwargs={'pk': self.kwargs['pk'],'pk2': self.kwargs['pk2']})

class DeleteStreetObjectView(BSModalDeleteView):
    model = StreetObject
    template_name = 'gallery/modals/delete_streetobject.html'
    success_message = 'Success: Se borro el objeto.'
    def get_success_url(self):
        return reverse("gallery:selectroi", kwargs={'pk': self.object.photo.photoset.id,'pk2': self.object.photo.index})
    

def deleteallobjects(request):
    print("PASA POR OBEJTODATA")
    pk = request.GET.get('pk')
    pk2 = request.GET.get('pk2')
    ps = PhotoSet.objects.get(id = pk)
    print("PK2")
    print(pk2)
    print(pk)
 
    parametrosPS=ParametersPhotoSet.objects.get(photoset=ps)
    
    parametrosPS.countLuminaria=0
    parametrosPS.countPostacion=0
    parametrosPS.countVehiculos=0
    parametrosPS.countOtros=0
    parametrosPS.lastPhotoDetect=0
    parametrosPS.statusDetection="stopped"
    parametrosPS.save()
    StreetObject.objects.filter(photoset = PhotoSet.objects.get(id = int(pk))).all().delete()
    
    return JsonResponse({'ok':'objetos eliminados'})
    

class ObjectsView(generic.ListView):
    model = Photo_pair
    template_name = 'gallery/view_objects.html'
    context_object_name = 'photopair'
    
    def get_context_data(self, **kwargs):
        context = super(ObjectsView, self).get_context_data(**kwargs)
        ps = PhotoSet.objects.get(id = self.kwargs['pk'])
        currentphoto=Photo_pair.objects.filter(photoset = ps).get(index=self.kwargs['pk2'])
        streetoctbje=StreetObject.objects.filter(photo_id = currentphoto).all().values_list('location_id')
        context['photopair'] = Photo_pair.objects.filter(photoset = ps).get(index=self.kwargs['pk2'])
        context['location'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']).location
        context['objetos'] = StreetObject.objects.filter(photo = context['photopair'])
        latitudeObjetos = [c.location.latitude for c in context['objetos']]
        longitudeObjetos = [c.location.longitude for c in context['objetos']]
        ObjectSelec=None
        try:
            m = generate_map_objetos(latitudeObjetos,longitudeObjetos,ObjectSelec)
            context['map'] = m._repr_html_()
        except:
            context['map'] = "Esta imagen no posee coordenadas"
        for lat, lon in zip(latitudeObjetos, longitudeObjetos):
            print(lat,lon)
        return context
    def get_queryset(self):
        return Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2'])
    def get_success_url(self):
        return reverse("gallery:selectroi", kwargs={'pk': self.kwargs['pk'],'pk2': self.kwargs['pk2']})

class ObjectDetectRois:
    def __init__(self, x, y,w,h,zdepth,xdepth,ddepth,latitude,longitude,label,conf):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.zdepth = zdepth
        self.xdepth =xdepth
        self.ddepth =ddepth
        self.latitude=latitude
        self.longitude=longitude
        self.label=label
        self.conf=conf

class DetectObjectViewManual(generic.ListView):
    modelo=None
    model = Photo_pair
    template_name = 'gallery/detectobjectmanual.html'
    context_object_name = 'photopair'
    
    #se usa para cargar el modelo primeramente antes que la vista
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if DetectObjectViewManual.modelo is None:
            device=''
            device = select_device(device)
            weights='./yolov/best.pt'
            DetectObjectView.modelo = attempt_load(weights, map_location=device)  # load FP32 model

    def get_context_data(self, **kwargs):
        context = super(DetectObjectViewManual, self).get_context_data(**kwargs)
        objectdetectroi=[]
        imageWidth=2666;
        imageHeight=2000;
        maxWidth=imageWidth*0.9
        minWidth=imageWidth-maxWidth
        maxHeight=imageHeight*0.75
        minDepth=3
        maxDepth=25
        ps = PhotoSet.objects.get(id = self.kwargs['pk'])
        context['next'] = min(self.kwargs['pk2']+1,Photo_pair.objects.filter(photoset = ps).latest('index').index)
        context['previous'] = max(self.kwargs['pk2']-1,0)
        context['location'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']).location
        context['photopair'] = Photo_pair.objects.filter(photoset = ps).get(index=self.kwargs['pk2'])
        image_r=(context['photopair'].image_r)
        image_l=(context['photopair'].image_l)
        imagen,objectsRoi,objectLabel,objectconf=detect(image_r,DetectObjectView.modelo)
        if self.kwargs['pk2']==0:
            context['location_next'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']+10).location
        else:
            context['location_next'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']+10).location
        #pilaLocation = Pila()
        for objeto,label,conf in zip(objectsRoi,objectLabel,objectconf):
            zdepth,xdepth,ddepth=depthwithframes(objeto.x,objeto.y,objeto.w,objeto.h,"/media/"+str(image_r),"/media/"+str(image_l))
            lat_new,lon_new=LatitudeLongitude(context['location'].latitude,context['location'].longitude,context['location_next'].latitude,context['location_next'].longitude,zdepth,xdepth)
            if zdepth<=maxDepth and zdepth>= minDepth and objeto.x>minWidth and objeto.x<maxWidth and objeto.y<maxHeight:
                
                #currentphoto=Photo_pair.objects.filter(photoset = ps).get(index=self.kwargs['pk2']-(i+1))
                context['photopair'] = Photo_pair.objects.filter(photoset = ps).get(index=self.kwargs['pk2'])
                context['objetos'] = StreetObject.objects.filter(photo = context['photopair'])
                obj = ObjectDetectRois(objeto.x,objeto.y,objeto.w,objeto.h,zdepth,xdepth,ddepth,lat_new,lon_new,label,conf)
                objectdetectroi.append(obj)
            
        context['objectsRoi'] =objectdetectroi

        try:
            #m = generate_map(ps = ps, ind=pk2,photos= pho, layers=lay)
            m = generate_map(ps, self.kwargs['pk2'],False)
            context['map'] = m._repr_html_()
        except:
            context['map'] = "Esta imagen no posee coordenadas"
        #context['map'] =map
        #cv2.imwrite('./media/detect.jpg', imagen)
        #context['objectdetect'] ='/media/detect.jpg'
        
        return context
    
    def get_success_url(self):
        return reverse("gallery:detectobject", kwargs={'pk': self.kwargs['pk'],'pk2': self.kwargs['pk2']})


class DetectObjectView(generic.ListView):
    modelo=None
    model = Photo_pair
    template_name = 'gallery/detectobject.html'
    context_object_name = 'photopair'
    
    def get_context_data(self, **kwargs):
        context = super(DetectObjectView, self).get_context_data(**kwargs)
        objectdetectroi=[]
        ps = PhotoSet.objects.get(id = self.kwargs['pk'])
        context['next'] = min(self.kwargs['pk2']+1,Photo_pair.objects.filter(photoset = ps).latest('index').index)
        context['previous'] = max(self.kwargs['pk2']-1,0)
        context['location'] = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = self.kwargs['pk'])).get(index=self.kwargs['pk2']).location
        context['photopair'] = Photo_pair.objects.filter(photoset = ps).get(index=self.kwargs['pk2'])
        image_r=(context['photopair'].image_r)
        image_l=(context['photopair'].image_l)
        
        try:
            #m = generate_map(ps = ps, ind=pk2,photos= pho, layers=lay)
            m = generate_map(ps, self.kwargs['pk2'],False)
            context['map'] = m._repr_html_()
        except:
            context['map'] = "Esta imagen no posee coordenadas"
        
        return context
    
    def get_success_url(self):
        return reverse("gallery:detectobject", kwargs={'pk': self.kwargs['pk'],'pk2': self.kwargs['pk2']})

def distanceObjects(request):
    urlRight = request.GET.get('urlRight')
    urlLeft = request.GET.get('urlLeft')
    xRight = request.GET.get('xRight')
    yRight = request.GET.get('yRight')
    wRight = request.GET.get('wRight')
    hRight = request.GET.get('hRight')
    xRight2 = request.GET.get('xRight2')
    yRight2 = request.GET.get('yRight2')
    wRight2 = request.GET.get('wRight2')
    hRight2 = request.GET.get('hRight2')
    zdepth1,x1,disp1=depthwithframes(xRight,yRight,wRight,hRight,urlRight,urlLeft)
    zdepth2,x2,disp2=depthwithframes(xRight2,yRight2,wRight2,hRight2,urlRight,urlLeft)
    distance=pow((pow(zdepth2-zdepth1,2)+pow(x2-x1,2)),1/2)
    print(distance)
    return JsonResponse({'distance':distance})

def zdepth(request):
    urlRight = request.GET.get('urlRight')
    urlLeft = request.GET.get('urlLeft')
    xRight = request.GET.get('xRight')
    yRight = request.GET.get('yRight')
    wRight = request.GET.get('wRight')
    hRight = request.GET.get('hRight')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    lat_next = request.GET.get('lat_next')
    lon_next = request.GET.get('lon_next')
    zdepth,x,disp=depthwithframes(xRight,yRight,wRight,hRight,urlRight,urlLeft)
    lat_new=0
    lon_new=0
    lat_new,lon_new=LatitudeLongitude(lat,lon,lat_next,lon_next,zdepth,x)
    print(zdepth,x,disp)
    return JsonResponse({'zdepth':zdepth,'x':x,'disp':disp,'lat_new':lat_new,'lon_new':lon_new})

def objectselec(request):
    print("PASA POR OBEJTODATA")
    pk = request.GET.get('pk')
    pk2 = request.GET.get('pk2')
    object = request.GET.get('object')
 
    ps = PhotoSet.objects.get(id = pk)
    currentphoto=Photo_pair.objects.filter(photoset = ps).get(index=pk2)
    Objects = StreetObject.objects.filter(photo = currentphoto)
    ObjectSelec=StreetObject.objects.filter(id=object)
    latitudeObjetos = [c.location.latitude for c in Objects]
    longitudeObjetos = [c.location.longitude for c in Objects]
    latitudeObjetos0 = [c0.location.latitude for c0 in ObjectSelec]
    longitudeObjetos0 = [c0.location.longitude for c0 in ObjectSelec]
    
    ObjectSelec=(latitudeObjetos0[0],longitudeObjetos0[0])
    try:
        m = generate_map_objetos(latitudeObjetos,longitudeObjetos,ObjectSelec)
        map = m._repr_html_()
    except:
        map = "Esta imagen no posee coordenadas"

    return JsonResponse({'map':map})

#def get_map(request):
#    object = int(request.GET.get('object'))
#    pk = request.GET.get('pk')
#    pk2 = request.GET.get('pk2')
#    ps = PhotoSet.objects.get(id = pk)
#    print(object)
#    pho = False
#    try:
#        lay = []
#        if object & 16: pho = True
#        if object & 8: lay.append(StreetObject.ObjectType.POSTACION)
#        if object & 4: lay.append(StreetObject.ObjectType.LUMINARIA)
#        if object & 2: lay.append(StreetObject.ObjectType.VEHICULO)
#        if object & 1: lay.append(StreetObject.ObjectType.OTROS)
#        m = generate_map(ps = ps, ind=pk2,photos= pho, layers=lay)
#        map = m._repr_html_()
#    except:
#        map = "Esta imagen no posee coordenadas"
#    return JsonResponse({'map':map})

                    
def startdetection(request):
    pk = request.GET.get('pk')
    pk2 = request.GET.get('pk2')
    total = request.GET.get('total')
    pk=int(pk)
    pk2=int(pk2)
    total=int(total)
    parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
    if parametrosPS.statusDetection == "stopped":
        parametrosPS.statusDetection="running"
        current=parametrosPS.lastPhotoDetect
        task=mitarea.delay(pk,current,total)
        taskId=task.id
        parametrosPS.tasksId=taskId
        parametrosPS.save() 
        request.session['taskId'] = taskId
        print("task ID: ",taskId)
        return JsonResponse({'taskId': "Nuevo proceso: "+taskId})
    taskId=parametrosPS.tasksId
    return JsonResponse({'taskId': "Ya en ejecucion: "+taskId})

def stopdetection(request):
    pk = request.GET.get('pk')
    pk=int(pk)
    parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
    taskId=parametrosPS.tasksId
    parametrosPS.statusDetection="stopped" 
    parametrosPS.save() 
    
    print("task ID: ",taskId)
 
    return JsonResponse({'taskId': "Procesos terminado: "+taskId})

def updateprogress(request):
    pk = request.GET.get('pk')
    pk2 = request.GET.get('pk2')
    total = request.GET.get('total')
    ps = PhotoSet.objects.get(id = pk)
    parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
    if parametrosPS.statusDetection != "stopped":
        actual=int(parametrosPS.lastPhotoDetect)
        progress=round((actual*100)/int(total))
        return JsonResponse({'progress':progress})
    
    return JsonResponse({'text':"Proceso terminado"})


def updateprogressmapa(request):
    pk = int(request.GET.get('pk'))
    pk2 = int(request.GET.get('pk2'))
    ps = PhotoSet.objects.get(id = pk)
    
    try:
        #m = generate_map(ps = ps, ind=pk2,photos= pho, layers=lay)
        lay = []
        m = generate_map(ps = pk, ind=pk2,photos= False)
        map = m._repr_html_()
    except:
        map = "Esta imagen no posee coordenadas"

    return JsonResponse({'map':map})

   
