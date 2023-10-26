function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data'));
}

var jsonPhotos = loadJson('#jsonData'); // lista que tiene cada objeto 'latitude': obj2.location.latitude,'longitude': obj2.location.longitude,'index': obj2.index,'tipo': "photo"
var jsonPostes = loadJson('#jsonData2');
var photocurrent = loadJson('#jsonData3');

var checkphotos = document.getElementById('checkphotos');
var checkposts = document.getElementById('checkposts');
var checklights = document.getElementById('checklights');
var btn_next = document.getElementById('btn-next');
var btn_prev = document.getElementById('btn-prev');
var image = document.getElementById('image');
var index_display = document.getElementById('index-display');
var selectroi = document.getElementById('selectroi');
var detectobject = document.getElementById('detectobject');

function createMarker(latlng, icon) {
  return L.marker(latlng, {icon: icon});
}

var currentindex = 0;
var dataset = 0;
var map;

function addMarkers(layer, positions, icon, tipo, current) {
  layer.clearLayers();
  for (var i = 0; i < positions.length; i++) {
    if(tipo==positions[i].tipo && i != current){
      var popupContent = "<button onclick='jumpto(" + positions[i].index +  ")' class='btn btn-secondary'>Go to photo</button>";
      createMarker([positions[i].latitude,positions[i].longitude], icon).addTo(layer).bindPopup(popupContent);
    }
  }
}

function addCurrentMarker(layer, position, icon) {
  layer.clearLayers();
  var popupContent = "<b>Current photo: </b>" + currentindex;
  createMarker([position.latitude,position.longitude], icon).addTo(layer).bindPopup(popupContent);
}

function updatemarkers(layer, json, icon, name) {
  addMarkers(layer, json, icon, name, currentindex);
}

function updatetext(htmlobject, text) {
  htmlobject.innerHTML = text;
}

function updateall(map, index)
{
  updatetext(btn_next,"Siguiente: " + Math.min(index + 1, jsonPhotos.length-1).toString());
  updatetext(btn_prev,"Anterior: " + Math.max(index - 1, 0).toString());
  image.src = jsonPhotos[index].url;
  map.panTo([jsonPhotos[index].latitude, jsonPhotos[index].longitude]);
  updatetext(index_display, index.toString());
  selectroi.href = "/images/" + dataset.toString() + "/" + index.toString() + "/selectroi/";
  detectobject.href = "/images/" + dataset.toString() + "/" + index.toString() + "/detectobject/";
}

function jumpto(index) {
  currentindex = index;
  updateall(map, currentindex);
}

document.addEventListener("DOMContentLoaded", function () {
  map = L.map('map2', {
    minZoom: 0,
    maxZoom: 30
  }).setView([ photocurrent[0].latitude,photocurrent[0].longitude], 18);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 22,
    maxNativeZoom: 19
  }).addTo(map);

  var mainLayer = L.layerGroup();
  var markersLayer1 = L.layerGroup();
  var markersLayer2 = L.layerGroup();
  var markersLayer3 = L.layerGroup();
  map.addLayer(mainLayer);
  map.addLayer(markersLayer1);
  map.addLayer(markersLayer2);
  map.addLayer(markersLayer3);

  var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconAnchor: [12, 41]
  });
  var redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconAnchor: [12, 41]
  });
  var blueIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [20, 36],
    iconAnchor: [10, 36]
  });
  var orangeIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconAnchor: [12, 41]
  });

  currentindex = photocurrent[0].photoindex;
  dataset = photocurrent[0].dataset;

  // Agregar marcadores iniciales
  updatemarkers(markersLayer1, jsonPhotos, blueIcon, "photo");
  addCurrentMarker(mainLayer, photocurrent[0], redIcon);

  updateall(map, currentindex);
  
  checkphotos.addEventListener('change', function () {
      if (this.checked) {
        updatemarkers(markersLayer1,jsonPhotos,blueIcon, "photo");
      } else {
        markersLayer1.clearLayers();
      }
  });

  checkposts.addEventListener('change', function () {
      if (this.checked) {
        updatemarkers(markersLayer2, jsonPostes,greenIcon, "postacion");
      } else {
        markersLayer2.clearLayers();
      }
  });

  checklights.addEventListener('change', function () {
    if (this.checked) {
      updatemarkers(markersLayer3, jsonPostes ,orangeIcon, "luminaria");
    } else {
      markersLayer3.clearLayers();
    }
  });

  btn_prev.addEventListener('click', function () {
    currentindex = Math.max(currentindex - 1, 0);
    if(checkphotos.checked){
    updatemarkers(markersLayer1,jsonPhotos, blueIcon, "photo");
    }
    else{
      markersLayer1.clearLayers();
    }
    addCurrentMarker(mainLayer, jsonPhotos[currentindex], redIcon);
    updateall(map, currentindex);
  });

  btn_next.addEventListener('click', function () {
    currentindex = Math.min(currentindex + 1, jsonPhotos.length-1);
    if(checkphotos.checked){
      updatemarkers(markersLayer1,jsonPhotos, blueIcon, "photo");
    }
    else{
      markersLayer1.clearLayers();
    }
    addCurrentMarker(mainLayer, jsonPhotos[currentindex], redIcon);
    updateall(map, currentindex);
  });

});

