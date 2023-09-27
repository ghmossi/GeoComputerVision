function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

function loadJson2(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json2'));
}

function loadJson3(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json3'));
}

function updatemap() {
  //resetMap();
  generatemap();
}

window.onload = function (){
  generatemap();
}


  var jsonData = loadJson('#jsonData');
  var jsonData2 = loadJson2('#jsonData2');
  var photocurrent = loadJson3('#jsonData3');
  console.log(photocurrent)

  var mapa = L.map('map2').setView([ photocurrent[0].latitude,photocurrent[0].longitude], 18);
function generatemap() {
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 30,
          attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(mapa);

      // Loop through positions from Django and add markers
var markerOptions = {
        //title: position.description,  // Tooltip
        riseOnHover: true,            // Elevate marker on hover
        opacity: 0.7                  // Opacity (adjust as needed)
};
  
  for(i=0;i<jsonData.length;i++){
    
    if (jsonData[i].latitude=== photocurrent[0].latitude&&jsonData[i].longitude=== photocurrent[0].longitude) {  // Replace 123 with the actual position ID
              markerOptions.icon = L.divIcon({
              className: 'custom-marker-icon',
              html: '<i class="fas fa-map-marker-alt" style="color: red;"></i>',
              iconSize: [32, 32],               // Adjust icon size as needed
              iconAnchor: [16, 32],             // Adjust icon anchor as needed
          });
    }
    var popupContent = "<b>Description:</b> dato <br>" +
                                 "<a href='/images/"+photocurrent[0].dataset+"/"+jsonData[i].index+"/'>Link to Example</a>";
        
    if (checkphoto.checked == true){
      
        L.marker([jsonData[i].latitude, jsonData[i].longitude],markerOptions)
              .addTo(mapa)
              .bindPopup(popupContent);
    }
          
  }
  if (checkposts.checked == true){
    console.log("CHECKED")
    markerOptions.icon = L.divIcon({
      className: 'custom-marker-icon2',
      html: '<u class="fas fa-map-marker-alt" style="color: red;"></i>',
      iconSize: [32, 32],               // Adjust icon size as needed
      iconAnchor: [16, 32]
    });
    for(i=0;i<jsonData2.length;i++){
        var popupContent = "<b>Description:</b> dato <br>" +
              "<a href='/images/"+photocurrent[0].dataset+"/"+jsonData2[i].index+"/'>Objeto</a>";
        L.marker([jsonData2[i].latitude, jsonData2[i].longitude],markerOptions)
              .addTo(mapa)
              .bindPopup(popupContent);
    }
  }

  
};

function resetMap() {
  // Elimina todas las capas y reinicia el mapa
  map.eachLayer(function (layer) {
      map.removeLayer(layer);
  });

  // Configura el mapa nuevamente
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
  }).addTo(mapa);

  // Restablece la vista del mapa
  L.map('map2').setView([ photocurrent[0].latitude,photocurrent[0].longitude], 18);

  // Puedes agregar aquí el código para volver a agregar capas, si es necesario
}