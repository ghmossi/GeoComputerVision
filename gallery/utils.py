import folium
from django.urls import reverse
from .models import *
import ezdxf

import cv2
import math
import numpy as np
from geographiclib.geodesic import Geodesic
import pyproj

def generate_map(ps,ind, photos = True, layers = [StreetObject.ObjectType.OTROS, StreetObject.ObjectType.POSTACION, StreetObject.ObjectType.LUMINARIA]):
    color_options = ['beige', 'black', 'blue', 'cadetblue', 'darkblue', 'darkgreen', 'darkpurple', 'darkred', 'gray', 'green', 'lightblue', 'lightgray', 'lightgreen', 'lightred', 'orange', 'pink', 'purple', 'white']
    currentphotopair = ps.album.get(index=ind) 
    loc = currentphotopair.get_location()
    m = folium.Map(location = loc,zoom_start = 18,control_scale=True,max_zoom=19)
    icon_red = folium.Icon(icon="user", icon_color='white', color="red", prefix="fa")
    folium.Marker(location = loc, icon=icon_red).add_to(m)    
    for photo_pair in ps.album.all():
        if photos == True:
            if photo_pair != ps.album.get(index=ind):
                loc_photo = photo_pair.get_location()
                icon_photo = folium.Icon(icon="eye", icon_color='white', color='blue', prefix="fa")
                popup2image = folium.Popup(html='<a href=' + reverse('gallery:image2', kwargs={'pk': ps.id, 'pk2':photo_pair.index})  +' target="_top">Ir a la imagen<a>')
                folium.Marker(location = loc_photo, icon = icon_photo, popup = popup2image).add_to(m)
        for object in photo_pair.img.all():
            for layer in layers:
                #layer_color=random.choice(color_options)
                #color_options.remove(layer_color)
                if layer ==StreetObject.ObjectType.OTROS: 
                    layer_color='darkgreen'
                if layer ==StreetObject.ObjectType.POSTACION: 
                    layer_color='darkpurple'
                if layer ==StreetObject.ObjectType.LUMINARIA: 
                    layer_color='orange'
                if layer ==StreetObject.ObjectType.VEHICULO: 
                    layer_color='black'               
                icon_layer = folium.Icon(icon="tower-broadcast", icon_color='white', color=layer_color, prefix="fa")
                if object.objtype == layer:
                    loc_object = object.get_location()
                    popup2image = folium.Popup(html= object.name +'<br>'+ object.description+'<br>'+'<a href=' + reverse('gallery:image2', kwargs={'pk': ps.id, 'pk2':photo_pair.index})  +' target="_top">Ir a la imagen<a>')
                    folium.Marker(location = loc_object, icon = icon_layer, popup = popup2image).add_to(m)
    return m

def generate_map_objetos(latitudeObjetos,longitudeObjetos,Obj_selec): 
    if Obj_selec ==None:
        loc = (latitudeObjetos[0],longitudeObjetos[0])
        m = folium.Map(location = loc,zoom_start = 19,control_scale=True,max_zoom=19)    
        folium.Marker(location = loc).add_to(m)
        for lat, lon in zip(latitudeObjetos, longitudeObjetos):
            print(lat,lon)
            #popup2image = folium.Popup(html='<a href=' + reverse('gallery:image2', kwargs={'pk': ps.id, 'pk2':photo_pair.index})  +' target="_top">Ir a la imagen<a>')
            folium.Marker(location= (lat,lon)).add_to(m)
    else:
        loc = Obj_selec
        m = folium.Map(location = loc,zoom_start = 19,control_scale=True,max_zoom=19)    
        folium.Marker(location = loc).add_to(m)
        for lat, lon in zip(latitudeObjetos, longitudeObjetos):
            print(lat,lon)
            #popup2image = folium.Popup(html='<a href=' + reverse('gallery:image2', kwargs={'pk': ps.id, 'pk2':photo_pair.index})  +' target="_top">Ir a la imagen<a>')
            folium.Marker(location= (lat,lon)).add_to(m)
        icon_red = folium.Icon(icon="info-sign", icon_color='white', color="red", prefix="fa")
        folium.Marker(location = loc, icon=icon_red).add_to(m)
    return m

def find_depth(circle_right, circle_left, frame_right, frame_left, baseline,f, alpha):
    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape
    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
    else:
        print('Left and right camera frames do not have the same pixel width')
    x_right = circle_right[0]
    x_left = circle_left[0]
    # CALCULATE THE DISPARITY:
    disparity = x_left-x_right      #Displacement between left and right frames [pixels]
    # CALCULATE DEPTH z:
    zDepth = (baseline*f_pixel)/disparity             #Depth in [cm]
    return disparity

def add_HSV_filter(frame, camera):
	# Blurring the frame
    blur = cv2.GaussianBlur(frame,(5,5),0) 
    # Converting RGB to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    l_b_r = np.array([60, 110, 50])        # Lower limit for red ball
    u_b_r = np.array([255, 255, 255])       # Upper limit for red ball
    l_b_l = np.array([143, 110, 50])        # Lower limit for red ball
    u_b_l = np.array([255, 255, 255])       # Upper limit for red ball
	#l_b = np.array([140, 106, 0])        # LOWER LIMIT FOR BLUE COLOR!!!
	#u_b = np.array([255, 255, 255])
	# HSV-filter mask
	#mask = cv2.inRange(hsv, l_b_l, u_b_l)
    if(camera == 1):
        mask = cv2.inRange(hsv, l_b_r, u_b_r)
    else:
        mask = cv2.inRange(hsv, l_b_l, u_b_l)
    # Morphological Operation - Opening - Erode followed by Dilate - Remove noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    return mask

def depthwithframes(x,y,w,h, frame_right,frame_left):
    print(frame_right)
    print(frame_left)
    color=(0,255,0)
    grosor=2
    ref=450
    ancho=2333
    alto=2000
    count = 0
    indice=0
    i=0
    Xdistancia=[0,0]
    Zdistancia=[0,0]
    #path='C:/Users/gmoss/Desktop/ProyectosDjango/Proyecto-Mi-Django-Gallery_v3/Mi-Django-gallery/'
    print("."+frame_right)
    Right_nice = cv2.imread("."+frame_right)
    #Right_nice=frameR.copy()
    x=int(x)
    y=int(y)
    w=int(w)
    h=int(h)
    cv2.rectangle(Right_nice, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite('./Right_nice.jpg', Right_nice)
    roi=Right_nice[y:y+h, x:x+w]
    xR=x+round(w/2)
    yR=y+round(h/2)
    Left_nice = cv2.imread("."+frame_left)
    #Left_nice=frameL.copy()
    gray_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_Left_nice = cv2.cvtColor(Left_nice, cv2.COLOR_BGR2GRAY)
    # Detect the ROI in the left camera image using template matching
    result = cv2.matchTemplate(gray_Left_nice, gray_roi, cv2.TM_CCOEFF_NORMED)
    # Get the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    x, y = max_loc
    cv2.rectangle(Left_nice, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite('./Left_nice.jpg', Left_nice)
    xL=x+round(w/2)
    yL=y+round(h/2)
    frame_rate = 1    #Camera frame rate (maximum at 120 fps)
    B = 20           #Dis0tance between the cameras [cm] si sube aumente la distancia
    f = 30              #C13era lense's focal length [mm]
    alpha = 95     #Camera field of view in the horisontal plane [degrees] si baja aumenta la distancia
    mask_right = add_HSV_filter(Right_nice, 1)
    mask_left = add_HSV_filter(Left_nice, 0)
    # Result-frames after applying HSV-filter mask
    res_right = cv2.bitwise_and(Right_nice, Right_nice, mask=mask_right)
    res_left = cv2.bitwise_and(Left_nice, Left_nice, mask=mask_left)
    circles_right =(xR,yR)
    circles_left =(xL,yL)


    disparity = find_depth(circles_right,circles_left,Right_nice, Left_nice, B, f, alpha)
    #image_width =2666
    image_width =2666
    alpha=120
    print("///////////////")
    #print("Disparity: ",disparity)
    cuadrante=image_width/2
    if xR<cuadrante:
        beta=(alpha/2)-((xR*(alpha/2))/float(cuadrante))
        grados = round(beta, 2)
        rad=math.radians(grados)
        ##print("cos a: ",math.cos(rad))
        #disparity = disparity *(1/math.cos(rad))
        phi=math.radians(-90+(grados))
        ##print("Grados: ",grados*-1)
        ##print("Disparity: ",disparity)

    if xR>cuadrante:
        beta=(alpha/2)-(((image_width-xR)*(alpha/2))/float(cuadrante))
        grados = round(beta, 2)
        rad=math.radians(grados)
        ##print("cos a: ",math.cos(rad))
        #disparity = disparity * (math.cos(rad))
        ##print("Grados: ",grados)
        ##print("Disparity: ",disparity)
       

    if xR==cuadrante:
        grados=0
        ##print("Grados: ",grados)
        ##print("Disparity: ",disparity)

    zdepth=DisparityDepth(disparity)
    if xR>cuadrante:
        x=math.sin(math.radians (grados))*zdepth
    if xR<cuadrante:
        x=-(math.sin(math.radians (grados))*zdepth)
    if xR==cuadrante:
        x=0
    x=x*math.cos(math.radians (55)-math.radians (grados))
    print("zdepth: ",zdepth," x: ",x," disparity: ",disparity)

    return round(zdepth,1),round(x,1),round(disparity,0) 

def DisparityDepth(disp):
    if disp > 61:
        m=-4.75
        b=99
        depth=(disp-b)/m
    if disp >37 & disp <= 61 :
        m=-4
        b=93
        depth=(disp-b)/m
    if disp <=37:
        m=-1
        b=51
        depth=(disp-b)/m
    return depth

def DisparityDepth_1333x1000(disp):
    if disp > 31:
        m=-2.25
        b=49
        depth=(disp-b)/m
    if disp >19 & disp <= 31 :
        m=-2
        b=47
        depth=(disp-b)/m
    if disp <=19:
        m=-0.56
        b=26.78
        depth=(disp-b)/m
    return depth

def LatitudeLongitude(lat,lon,lat_next,lon_next,z,x):
    A = (float(lat),float(lon))
    B = (float(lat_next),float(lon_next))
    #print(A,B)

    s= z
    #Define the ellipsoid
    geod = Geodesic.WGS84

    #Solve the Inverse problem
    inv = geod.Inverse(A[0],A[1],B[0],B[1])
    #deno sumarle angulo al azimut desde 90 a -90
    azi1 = (inv['azi1'])
    #print('Initial Azimuth from A to B = ' + str(azi1))

    #Solve the Direct problem
    dir = geod.Direct(A[0],A[1],azi1,s)

    C = (dir['lat2'],dir['lon2'])
    
    if x<0:
        azimuth_perpendicular = azi1 - 90  # Sumar 90 grados para obtener el acimut perpendicular
    if x>0:
        azimuth_perpendicular = azi1 + 90  # Restar 90 grados para obtener el acimut perpendicular
    
    # Calcular el nuevo punto en función de la distancia perpendicular y el acimut
    dirper = geod.Direct(dir['lat2'], dir['lon2'], azimuth_perpendicular, abs(x))

    C = (dirper['lat2'],dirper['lon2'])   
    
    print('GPS =' + str(C))
    return C

# utils.py
class Pila:
    def __init__(self):
        self.items = []

    def push(self, item):
        if len(self.items) < 50:
            self.items.append(item)
        else:
            # Si la pila está llena, eliminamos el elemento más antiguo
            self.items.pop(0)

    def pop(self):
        if not self.is_empty():
            return self.items.pop(-1)  # Corrección aquí, elimina el último elemento de la lista

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_items(self):
        return self.items[:]
    
    
def distanceTwoLocations(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Radio de la Tierra en metros (aproximado)
    radius = 6371000

    # Diferencias de latitud y longitud
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(d_lat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distancia en metros
    distance = radius * c
    return distance

def generate_DXF(path,ps):
    doc = ezdxf.new(setup=True)
    photos = True # Si se pone en false no se agregan las fotos al dxf
    doc.layers.add(name="Photos", color=7)
    doc.layers.add(name=StreetObject.ObjectType.POSTACION, color=6)
    doc.layers.add(name=StreetObject.ObjectType.LUMINARIA, color=5)
    doc.layers.add(name=StreetObject.ObjectType.VEHICULO, color=4)
    doc.layers.add(name=StreetObject.ObjectType.OTROS, color=3)

    photo = doc.blocks.new(name='PHOTO')
    photo.add_lwpolyline([(2, -1), (2, 1)])  # the flag symbol as 2D polyline
    photo.add_lwpolyline([(2, 1), (-2, 1)])  # the flag symbol as 2D polyline
    photo.add_lwpolyline([(-2, 1), (-2, -1)])  # the flag symbol as 2D polyline
    photo.add_lwpolyline([(-2, -1), (2, -1)])  # the flag symbol as 2D polyline
    photo.add_circle((0, 0), 1)  # mark the base point with a circle

    recorrido = doc.blocks.new(name='RECORRIDO')

    obj = doc.blocks.new(name='OBJECT')
    obj.add_lwpolyline([(1, 0), (-1, 0)])  # the flag symbol as 2D polyline
    obj.add_lwpolyline([(0, 1), (0, -1)])  # the flag symbol as 2D polyline
    obj.add_circle((0, 0), 1)  # mark the base point with a circle
    
    msp = doc.modelspace()

    if photos == True:
        photos_points = [dxfcoord(photopair.get_location()) for photopair in ps.album.all()]
    object_points = []
    for photopair in ps.album.all():
        for obj in photopair.img.all():
            obj_loc = (dxfcoord(obj.get_location()), obj.objtype)#.append(obj.objtype)
            object_points.append(obj_loc)
    scale = 1
    if photos == True:
        # for point in photos_points:
        #     msp.add_blockref('PHOTO', point, dxfattribs={
        #         'xscale': scale,
        #         'yscale': scale,
        #         'rotation': 0,
        #         "layer": "Photos"
        #     })
        recorrido.add_lwpolyline(photos_points)
        msp.add_lwpolyline(photos_points, dxfattribs={
            "layer": "Photos"
        })
        # msp.add_blockref('RECORRIDO',photos_points[0],dxfattribs={
        #     'xscale': 1,
        #     'yscale': 1,
        #     'rotation': 0,
        #     "layer":  "Photos"
        # })    

    for point in object_points:
        msp.add_blockref('OBJECT', point[0], dxfattribs={
            'xscale': scale,
            'yscale': scale,
            'rotation': 45,
            "layer": point[1]
        })
    doc.saveas(path)

def dxfcoord(loc):
    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32721") # ESTO SOLO FUNCIONA PARA UN PEDAZO DE ARGENTINA, HAY QUE CAMBIAR EL PARAMETRO DE LA DERECHA DEPENDIENDO DE LA UBICACION
    return transformer.transform(loc[0], loc[1])


