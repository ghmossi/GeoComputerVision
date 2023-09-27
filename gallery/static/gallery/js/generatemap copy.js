//var mapElement = document.getElementById('map2');
//var positionsPhotos = mapElement.getAttribute('positionsPhotos');

var  positionsPhotos ='

 

var photopairLatitudeElement = document.getElementById('photopair-latitude');
var photopairLatitude = photopairLatitudeElement.getAttribute('photopairLatitude');

var photopairLongitudeElement = document.getElementById('photopair-longitude');
var photopairLongitude = photopairLongitudeElement.getAttribute('photopairLongitude');

var photopairIndexElement = document.getElementById('photopair-index');
var photopairIndex = photopairIndexElement.getAttribute('photopairIndex');

var photosetIndexElement = document.getElementById('photoset-index');
var photosetIndex = photosetIndexElement.getAttribute('photosetIndex');

var dato=positionsPhotos[0]
console.log(positionsPhotos)
console.log(dato)
var mapa = L.map('map2').setView([ photopairLatitude,photopairLongitude], 18);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 30,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mapa);


for (var i = 0; i < positionsPhotos.length; i++) {
  console.log(positionsPhotos.length)
  var lat = positionsPhotos[i][0];
  var lon = positionsPhotos[i][1];

  console.log("lat: "+lat+" lon: "+lon)

  
  var markerOptions = {
        //title: position.description,  // Tooltip
        riseOnHover: true,            // Elevate marker on hover
        opacity: 0.7                  // Opacity (adjust as needed)
  };
  if (lat=== photopairLatitude &&lon=== photopairLongitude ) {  
        markerOptions.icon = L.divIcon({
            className: 'custom-marker-icon',
            html: '<i class="fas fa-map-marker-alt" style="color: red;"></i>',
            iconSize: [32, 32],               // Adjust icon size as needed
            iconAnchor: [16, 32],             // Adjust icon anchor as needed
        });
    }
    var popupContent = "<b>Description:</b> dato <br>" +
                               "<a href='/images/"+photosetIndex+"/"+photopairIndex+"/'>Link to Example</a>";
        L.marker([lat, lon],markerOptions)
            .addTo(mapa)
            .bindPopup(popupContent);
        
  }

