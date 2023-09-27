from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gallery.models import PhotoSet
from .models import Map
from .forms import CreateMap
import folium
from folium.plugins import FastMarkerCluster
from GPSPhoto import gpsphoto


# Create your views here.

@login_required(login_url='/users/login/')
def map(request):
    if request.method == 'POST':
        form = CreateMap(request.POST,user=request.user)
        if form.is_valid():

            ps = form.cleaned_data.get('title')
            map = Map.objects.create(meta = "")
            map.meta += "Data Set: " + ps.title
            map.meta += ", con " + str(ps.album.count()) + " fotos."

            tooltip = "Ver foto"

            folder = 'media\ '
            imageurls = [folder[:len(folder)-1] + str(image.image_r) for image in ps.album.all()]

            latitudes = [gpsphoto.getGPSData(imageurl)["Latitude"] for imageurl in imageurls]
            longitudes = [gpsphoto.getGPSData(imageurl)["Longitude"] for imageurl in imageurls]
            coords = list(zip(latitudes,longitudes))

            centerpoint = [sum(latitudes)/len(latitudes),sum(longitudes)/len(longitudes)]

            m = folium.Map(location = centerpoint,zoom_start = 19,control_scale=True,max_zoom=19)
            m.add_child(folium.LatLngPopup())
            for coord in coords:
                popup = "\n Lat:" + str(coord[0]) + ", Lon:" + str(coord[1]) 
                folium.Marker(coord, popup=popup, tooltip=tooltip).add_to(m)

            map.meta += "\n Lat:" + str(centerpoint[0])
            map.meta += "\n Lon:" + str(centerpoint[1]) 
            context = {'map':m._repr_html_(),'meta':map}
            return render(request,'maps/map.html',context)
    else:
        form = CreateMap(user=request.user)
    return render(request, 'maps/choose_set.html',{'form': form})
