function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

function loadJson2(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json2'));
}

function loadJson3(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json3'));
}




var jsonPhotos = loadJson('#jsonData');
var jsonPostes = loadJson2('#jsonData2');
var photocurrent = loadJson3('#jsonData3');


document.addEventListener("DOMContentLoaded", function () {
  var map = L.map('map2', {
    minZoom: 0,
    maxZoom: 30
}).setView([ photocurrent[0].latitude,photocurrent[0].longitude], 18);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 22,
    maxNativeZoom: 19
  }).addTo(map);

  var checkphotos = document.getElementById('checkphotos');
  var checkposts = document.getElementById('checkposts');
  var checklights = document.getElementById('checklights');


  var markersLayer1 = L.layerGroup();
  var markersLayer2 = L.layerGroup();
  var markersLayer3 = L.layerGroup();
  map.addLayer(markersLayer1);
  map.addLayer(markersLayer2);
  map.addLayer(markersLayer3);


  function addMarkers(layer, positions, color,pk,tipo) {
      layer.clearLayers();
      
      for (var i = 0; i < positions.length; i++) {
        if(tipo==positions[i].tipo){
            var popupContent = "<b>Description:</b>"+tipo+ "<br>" +
                                 "<a href='/images/"+pk+"/"+positions[i].index+"/'>Link to Example</a>";
              L.marker([positions[i].latitude,positions[i].longitude], { icon: createColoredIcon(color) }).addTo(layer).bindPopup(popupContent);;
        }
      }
  }

  function addMarkers2(layer, positions, color,pk,tipo) {
    layer.clearLayers();
    
    for (var i = 0; i < positions.length; i++) {
      if(tipo==positions[i].tipo){
          var popupContent = "<b>Description:</b>"+tipo+ "<br>" +
                               "<a href='/images/"+pk+"/"+positions[i].index+"/'>Link to Example</a>";
            L.marker([positions[i].latitude,positions[i].longitude], { icon: createColoredIcon3(color) }).addTo(layer).bindPopup(popupContent);;
      }
    }
}

  function addCurrentMarkers(layer, positions, color,pk) {
      var popupContent = "<b>Description:</b> dato <br>" +
                               "<a href='/images/"+pk+"/"+positions.index+"/'>Link to Example</a>";
        L.marker([positions.latitude,positions.longitude], { icon: createColoredIcon2(color) }).addTo(layer).bindPopup(popupContent);;
    
}

  function createColoredIcon(color) {
    return L.divIcon({
        className: 'custom-icon',
        iconSize: [25, 41],
        html: '<div class="fas fa-map-marker-alt" style="color: ' + color + ';"></div>',
        iconAnchor: [12, 41]
    });

}

function createColoredIcon2(color) {
  return L.divIcon({
      className: 'custom-icon2',
      iconSize: [25, 41],
      html: '<div class="fas fa-map-marker-alt" style="color: ' + color + ';"></div>',
      iconAnchor: [12, 41]
  });
}

function createColoredIcon3(color) {
  return L.divIcon({
      className: 'custom-icon3',
      iconSize: [25, 41],
      html: '<div class="fas fa-map-marker-alt" style="color: ' + color + ';"></div>',
      iconAnchor: [12, 41]
  });
}

  // Agregar marcadores iniciales
  addMarkers(markersLayer1, jsonPhotos, 'blue',photocurrent[0].dataset,"photo");
  var currrent={
    'latitude':photocurrent[0].latitude,
    'longitude':photocurrent[0].longitude,
    'index':photocurrent[0].dataset
  }
  addCurrentMarkers(markersLayer1, currrent, 'red',photocurrent[0].dataset);
  //addMarkers(markersLayer2, jsonPostes);

checkphotos.addEventListener('change', function () {
    if (this.checked) {
        addMarkers(markersLayer1, jsonPhotos, 'blue',photocurrent[0].dataset,"photo");
        var currrent={
          'latitude':photocurrent[0].latitude,
          'longitude':photocurrent[0].longitude,
          'index':photocurrent[0].dataset
        }
        addCurrentMarkers(markersLayer1, currrent, 'red',photocurrent[0].dataset);
    } else {
        markersLayer1.clearLayers();
    }
});

checkposts.addEventListener('change', function () {
    if (this.checked) {
        addMarkers2(markersLayer2, jsonPostes,  'green',photocurrent[0].dataset,"postacion");
        var currrent={
          'latitude':photocurrent[0].latitude,
          'longitude':photocurrent[0].longitude,
          'index':photocurrent[0].dataset
        }
        addCurrentMarkers(markersLayer2, currrent, 'red',photocurrent[0].dataset)
    } else {
        markersLayer2.clearLayers();
    }
});

checklights.addEventListener('change', function () {
  if (this.checked) {
      addMarkers2(markersLayer3, jsonPostes,  'orange',photocurrent[0].dataset,"luminaria");
      var currrent={
        'latitude':photocurrent[0].latitude,
        'longitude':photocurrent[0].longitude,
        'index':photocurrent[0].dataset
      }
      addCurrentMarkers(markersLayer3, currrent, 'red',photocurrent[0].dataset)
  } else {
      markersLayer3.clearLayers();
  }
});

});

