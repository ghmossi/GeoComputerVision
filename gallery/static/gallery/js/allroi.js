var tabla = document.getElementById('tabla-datos');
var filas = tabla.getElementsByTagName('tr');
console.log("numero de filas",filas.length);
var nombres = [];
var center_x=0
var center_y=0
var width=0
var height=0
var imageWidthOriginal=2666;
//var imageWidthOriginal=1333;
var imageHeightOriginal=2000;
//var imageHeightOriginal=1000;
var originalWidth = 900;
var originalHeight = 675;
var factorOriginal=originalWidth/imageWidthOriginal;
const array_x=[];
const array_y=[];
const array_h=[];
const array_w=[];
var selec_x=0;
var selec_y=0;
var selec_w=0;
var selec_h=0;

// Iterar sobre las filas, empezando desde 1 para omitir la fila de encabezado
var canvas = document.getElementById("canvas");
    canvas.width = 900;
    //canvas.height = 675;
    var ctx = canvas.getContext("2d");
    var img = new Image();

    img.src= document.getElementById("urlRight").value;
    console.log(img)
    //img.onload = function() {
      //ctx.drawImage(img, 0, 0,900,675);
    //};

for (var i = 1; i < filas.length; i++) {
  var celdas = filas[i].getElementsByTagName('td');
  center_x = celdas[3].innerText;
  array_x[i]=center_x;
  console.log(center_x);
  center_y = celdas[4].innerText;
  array_y[i]=center_y;
  console.log(center_y);
  width = celdas[5].innerText;
  array_w[i]=width;
  console.log(width);
  height = celdas[6].innerText;
  array_h[i]=height;
  console.log(height);
}

function init() {
      originalWidth = 900;
      originalHeight = 675;
      zoomFit();
    }
function zoomFit() {
      draw();
    }

init();

function draw() {
      img.src = document.getElementById("urlRight").value;
      img.onload = function() {
      //ctx.clearRect(0, 0, canvas.width, canvas.height);
      var scaledWidth = originalWidth 
      var scaledHeight = originalHeight
      ctx.drawImage(img, 0, 0, scaledWidth, scaledHeight);
      for (var i = 1; i < filas.length; i++){
        var x = array_x[i]*factorOriginal ;
        var y = array_y[i] *factorOriginal;
        var w = array_w[i]*factorOriginal;
        var h= array_h[i]*factorOriginal;
        ctx.strokeStyle = 'magenta';
        ctx.lineWidth = 2;
        ctx.strokeRect(x,y,w,h);
        }
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 2;
        ctx.strokeRect(selec_x*factorOriginal,selec_y*factorOriginal,selec_w*factorOriginal,selec_h*factorOriginal);      }
    }
/*
var filas2 = document.querySelectorAll('#tabla-datos tbody tr');

    filas2.forEach(function(fila) {
      fila.addEventListener('click', function() {
        // Obtener las celdas de la fila
        var celdas = this.getElementsByTagName('td');
        
        console.log(celdas[0].innerText)
        selec_x=celdas[3].innerText
        selec_y=celdas[4].innerText
        selec_w=celdas[5].innerText
        selec_h=celdas[6].innerText
        //document.getElementById("lat").setAttribute('value',celdas[6].innerText);
        //document.getElementById("lon").setAttribute('value',celdas[7].innerText);
        draw();
      });
    });
  */


    function mostrarContenido(boton) {
      var pk= document.getElementById("pk").value;
      var pk2= document.getElementById("pk2").value;
      var fila = boton.parentNode.parentNode;
      var celdas = fila.getElementsByTagName("td");
      var object = "";
      object += celdas[9].innerHTML + " ";
      selec_x=celdas[3].innerText
      selec_y=celdas[4].innerText
      selec_w=celdas[5].innerText
      selec_h=celdas[6].innerText
      console.log(object)
      console.log(pk)
      console.log(pk2)
      draw();
      enviarDatosAlBackend(pk,pk2,object);

    }

    async function enviarDatosAlBackend(pk,pk2,object) {
   
      try {
        const response = await fetch(`/objectselec/?object=${object}&pk=${pk}&pk2=${pk2}`);
        const data = await response.json();
        if (data.map) {
          document.querySelector('div.map-container').innerHTML=(data.map)
          console.log(data.map);
        } else {
          console.log("No hay datos");
        }
      } catch (error) {
        console.log(error.message);
      }
    }
   