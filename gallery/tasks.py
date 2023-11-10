from celery import shared_task
import time
from .models import *
from .utils import *
from yolov.mydetect import detect
from yolov.models.experimental import attempt_load
from yolov.utils.torch_utils import select_device

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

@shared_task
def mitarea(pk,pk2,total):
    parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
    if parametrosPS.statusDetection=="running": 
        ps = PhotoSet.objects.get(id = pk)
        pk2=pk2+1
        objectdetectroi=[]
        device=''
        device = select_device(device)
        weights='./yolov/best.pt'
        modelo = attempt_load(weights, map_location=device)  # load FP32 model
        #parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
        #current=
        #parametrosPS.lastPhotoDetect=0
        #parametrosPS.save()
        fin=total-1
        inicio=pk2
        imageWidth=2666;
        imageHeight=2000;
        maxWidth=imageWidth*0.9
        minWidth=imageWidth-maxWidth
        maxHeight=imageHeight*0.75
        minDepth=6
        maxDepth=13
        minDistance=3
        maxDistance=6
        difAzimuth=5
        for current in range(inicio, fin):
            parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
            if parametrosPS.statusDetection=="stopped": 
                break
            parametrosPS.lastPhotoDetect=current+1
            parametrosPS.save()
            #location = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current).location
            photopair = Photo_pair.objects.filter(photoset = ps).get(index=current)
            image_r=(photopair.image_r)
            image_l=(photopair.image_l)
            imagen,objectsRoi,objectLabel,objectconf=detect(image_r,modelo)
            
            #location=Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current).location
            #location_next = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current+10).location
            #azimuthCurrent=Azimuth(location.latitude,location.longitude,location_next.latitude,location_next.longitude)
            #location5=Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current+5).location
            #location_next5 = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current+15).location
            #azimuthCurrent5=Azimuth(location5.latitude,location5.longitude,location_next5.latitude,location_next5.longitude)
            

            for objeto,label,conf in zip(objectsRoi,objectLabel,objectconf):
                # pongo finltro para descartar clases a detectar
                if label !="luminaria":
                    try:
                        location=Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current).location
                        zdepth,xdepth,ddepth=depthwithframes(objeto.x,objeto.y,objeto.w,objeto.h,"/media/"+str(image_r),"/media/"+str(image_l)) 
                        loc,azimuth=LatitudeLongitude2(ps,current,zdepth,xdepth,15)
                        print("PASO POR ESTE PUNTO")
                        nothing,azimuthNext=LatitudeLongitude2(ps,current+1,zdepth,xdepth,15)
                        if abs(azimuthNext - azimuth) <= difAzimuth:
                            difDistance=minDistance
                        else:
                            difDistance=maxDistance
                        print("PASO POR ESTE PUNTO2")
                        if zdepth<=maxDepth and zdepth>= minDepth and objeto.x>minWidth and objeto.x<maxWidth and objeto.y<maxHeight:
                            print("DETECT"," "+label+" "," "+conf+" ")
                            save=True
                            objetos = StreetObject.objects.filter(photoset = PhotoSet.objects.get(id = pk),objtype=label)
                            latitudeObjetos = [c.location.latitude for c in objetos]
                            longitudeObjetos = [c.location.longitude for c in objetos]
                            namesObjetos = [c.name for c in objetos]
                            for lat, lon,nameobj in zip(latitudeObjetos, longitudeObjetos,namesObjetos):
                                distance=distanceTwoLocations(lat, lon, loc[0], loc[1])
                                print("distancia:"," "+label+"-"+nameobj)
                                print(distance)
                                if distance<=difDistance:
                                    save=False
                            if save==True:
                                roi = Roi.objects.create(center_x = objeto.x,center_y = objeto.y,width = objeto.w,height = objeto.h)
                                photo = Photo_pair.objects.filter(photoset = pk).get(index=current)
                                loc = Location.objects.create(latitude = loc[0],longitude = loc[1])
                                parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
                                contador=0
                                if label == "luminaria":
                                    contador=int(parametrosPS.countLuminaria)+1
                                    parametrosPS.countLuminaria=contador
                                    parametrosPS.save()
                                elif label == "postacion":
                                    contador=int(parametrosPS.countPostacion)+1
                                    parametrosPS.countPostacion=contador
                                    parametrosPS.save()

                                nameObject=label+"_"+str(contador)
                                StreetObject.objects.create(name = nameObject,photoset = PhotoSet.objects.get(id = pk), photo = photo, description = label, location = loc,roi=roi, objtype = label)
                                obj = ObjectDetectRois(objeto.x,objeto.y,objeto.w,objeto.h,zdepth,xdepth,ddepth,loc[0],loc[1],label,conf)                    
                                objectdetectroi.append(obj)
                    except:
                        print("hubo error en calculo de profundidad")
            if current == fin:
                parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
                parametrosPS.statusDetection=="terminated"
                parametrosPS.save()

                
def nada(pk,pk2,total):
    parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
    if parametrosPS.statusDetection=="running": 
        ps = PhotoSet.objects.get(id = pk)
        pk2=pk2+1
        objectdetectroi=[]
        device=''
        device = select_device(device)
        weights='./yolov/best.pt'
        modelo = attempt_load(weights, map_location=device)  # load FP32 model
        #parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
        #current=
        #parametrosPS.lastPhotoDetect=0
        #parametrosPS.save()
        fin=total-1
        inicio=pk2
        imageWidth=2666;
        imageHeight=2000;
        maxWidth=imageWidth*0.9
        minWidth=imageWidth-maxWidth
        maxHeight=imageHeight*0.75
        minDepth=6
        maxDepth=13
        minDistance=3.5
        for current in range(inicio, fin):
            parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
            if parametrosPS.statusDetection=="stopped": 
                break
            parametrosPS.lastPhotoDetect=current+1
            parametrosPS.save()
            location = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current).location
            photopair = Photo_pair.objects.filter(photoset = ps).get(index=current)
            image_r=(photopair.image_r)
            image_l=(photopair.image_l)
            imagen,objectsRoi,objectLabel,objectconf=detect(image_r,modelo)
            
            location=Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current).location
            location_next = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current+10).location
            azimuthCurrent=Azimuth(location.latitude,location.longitude,location_next.latitude,location_next.longitude)
            location5=Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current+5).location
            location_next5 = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=current+15).location
            azimuthCurrent5=Azimuth(location5.latitude,location5.longitude,location_next5.latitude,location_next5.longitude)
            if abs(azimuthCurrent - azimuthCurrent5) <= 10:
                print("DIFERENCIA: ",str(abs(azimuthCurrent - azimuthCurrent5)))
                indexNext=current+10
            else:
                print("DIFERENCIA: ",str(abs(azimuthCurrent - azimuthCurrent5)))
                indexNext=current+5

            for objeto,label,conf in zip(objectsRoi,objectLabel,objectconf):
                # pongo finltro para descartar clases a detectar
                if label !="luminaria":
                    try:
                        zdepth,xdepth,ddepth=depthwithframes(objeto.x,objeto.y,objeto.w,objeto.h,"/media/"+str(image_r),"/media/"+str(image_l)) 
                        
                        if current < (fin-10):
                            location_next = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=indexNext).location
                            lat_new,lon_new=LatitudeLongitude(location.latitude,location.longitude,location_next.latitude,location_next.longitude,zdepth,xdepth)
                        else:
                            indexNext=current-10
                            location_previus = Photo_pair.objects.filter(photoset = PhotoSet.objects.get(id = pk)).get(index=indexNext).location
                            lat_new,lon_new=LatitudeLongitude(location_previus.latitude,location_previus.longitude,location.latitude,location.longitude,zdepth,xdepth)
             
                        if zdepth<=maxDepth and zdepth>= minDepth and objeto.x>minWidth and objeto.x<maxWidth and objeto.y<maxHeight:
                            print("DETECT"," "+label+" "," "+conf+" ")
                            save=True
                            objetos = StreetObject.objects.filter(photoset = PhotoSet.objects.get(id = pk),objtype=label)
                            latitudeObjetos = [c.location.latitude for c in objetos]
                            longitudeObjetos = [c.location.longitude for c in objetos]
                            namesObjetos = [c.name for c in objetos]
                            for lat, lon,nameobj in zip(latitudeObjetos, longitudeObjetos,namesObjetos):
                                distance=distanceTwoLocations(lat, lon, lat_new, lon_new)
                                print("distancia:"," "+label+"-"+nameobj)
                                print(distance)
                                if distance<=minDistance:
                                    save=False
                            if save==True:
                                roi = Roi.objects.create(center_x = objeto.x,center_y = objeto.y,width = objeto.w,height = objeto.h)
                                photo = Photo_pair.objects.filter(photoset = pk).get(index=current)
                                loc = Location.objects.create(latitude = lat_new,longitude = lon_new)
                                parametrosPS=ParametersPhotoSet.objects.get(photoset=pk)
                                contador=0
                                if label == "luminaria":
                                    contador=int(parametrosPS.countLuminaria)+1
                                    parametrosPS.countLuminaria=contador
                                    parametrosPS.save()
                                elif label == "postacion":
                                    contador=int(parametrosPS.countPostacion)+1
                                    parametrosPS.countPostacion=contador
                                    parametrosPS.save()

                                nameObject=label+"_"+str(contador)
                                StreetObject.objects.create(name = nameObject,photoset = PhotoSet.objects.get(id = pk), photo = photo, description = label, location = loc,roi=roi, objtype = label)
                                obj = ObjectDetectRois(objeto.x,objeto.y,objeto.w,objeto.h,zdepth,xdepth,ddepth,lat_new,lon_new,label,conf)                    
                                objectdetectroi.append(obj)
                    except:
                        print("hubo error en calculo de profundidad")


