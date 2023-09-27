imagename = "media\img_53_Cam2Path1.jpg"

from GPSPhoto import gpsphoto


data = gpsphoto.getGPSData(imagename)
print(data["Latitude"])
print(data["Longitude"])