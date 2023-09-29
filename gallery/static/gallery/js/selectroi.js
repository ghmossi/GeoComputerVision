var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    var img = new Image();
    canvas.width = 900;

    img.src= document.getElementById("urlRight").value;
    console.log(img)
    img.onload = function() {
      ctx.drawImage(img, 0, 0);
    };
    
    var originalWidth = 1;
    var originalHeight = 1;
    var zoomFactor = 1;
    var zoonCounter=0;
    var offsetX = 0;
    var offsetY = 0;
    var selection = null;
    var selection2 = null;
    var dato=null;
    var dato2=null;
    var isDragging = false;
    var isDragging2 = false;
    let isDraggingMov = false;
    let offsetXMov = 0;
    let offsetYMov = 0;
    var originx=0;
    var originy=0;
    var originx2=0;
    var originy2=0;
    var selectOneROI=true;
    var selectTwoROI=false;
  
    var imageWidth=900;
    //var imageWidthOriginal=2666;
    var imageWidthOriginal=1333;
    var imageHeight=675;
    //var imageHeightOriginal=2000;
    var imageHeightOriginal=1000;
    var factorX=imageWidth/imageWidthOriginal;
    var factory=imageHeight/imageHeightOriginal;

    function RoiDistancia() {
      var ratio2 = document.getElementById("roidistancia");
      if (ratio2.checked == true){
        console.log("roidistancia")
        document.getElementById("distanceObjects").setAttribute('value',true);
        selectTwoROI=true;
        selectOneROI=false;
      } else {
        document.getElementById("distanceObjects").setAttribute('value',false);
        selectTwoROI=false;
        selectOneROI=true;
      }
    }
    
    $(document).keydown(function(event) {
      if (event.key == "a") {
        movLeft()
      } else if (event.key == "d") {
        movRight()
      }else if (event.key == "w") {
        movUp()
      }else if (event.key == "s") {
        movDown()
      }
  });
    

    canvas.addEventListener('mousedown', function(e) {
    if(selectOneROI==true){  
      if (e.button === 0){
        isDragging = true;
        var rect = canvas.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
 
        originx=x*(imageWidth/rect.width);
        originy=y*(imageHeight/rect.height);
        selection = { x: originx, y: originy, width: 0, height: 0 };
        dato={ x: x, y: y, width: 0, height: 0 };
      }
    }
    if(selectTwoROI==true){  
      if (e.button === 0){
        isDragging2 = true;
        var rect = canvas.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        originx2=x*(imageWidth/rect.width);
        originy2=y*(imageHeight/rect.height);
        selection2 = { x: originx2, y: originy2, width: 0, height: 0 };
        dato2={ x: x, y: y, width: 0, height: 0 };
      }
    }
    });

    canvas.addEventListener('mousemove', function(e) {
      if(selectOneROI==true){ 
        if (isDragging) {
          draw();
          var rect = canvas.getBoundingClientRect();
          var x = e.clientX - rect.left;
          var y = e.clientY - rect.top;
          
          originx=x*(imageWidth/rect.width);
          originy=y*(imageHeight/rect.height);
          selection.width = originx - selection.x;  
          selection.height = originy - selection.y;
          dato.width=x- dato.x;
          dato.height=y- dato.y;
          document.getElementById("xRight").setAttribute('value',Math.trunc(dato.x*(imageWidthOriginal/rect.width)));
          document.getElementById("yRight").setAttribute('value',Math.trunc(dato.y*(imageHeightOriginal/rect.height)));
          document.getElementById("wRight").setAttribute('value',Math.trunc(dato.width*(imageWidthOriginal/rect.width)));
          document.getElementById("hRight").setAttribute('value',Math.trunc(dato.height*(imageHeightOriginal/rect.height)));
           }
      }
      if(selectTwoROI==true){ 
      if (isDragging2) {
          draw2();
          var rect = canvas.getBoundingClientRect();
          var x = e.clientX - rect.left;
          var y = e.clientY - rect.top;
          originx2=x*(imageWidth/rect.width);
          originy2=y*(imageHeight/rect.height);
          selection2.width = originx2 - selection2.x;
          selection2.height = originy2 - selection2.y;
          dato2.width=x- dato2.x;
          dato2.height=y- dato2.y;
          document.getElementById("xRight2").setAttribute('value',Math.trunc(dato2.x*(imageWidthOriginal/rect.width)));
          document.getElementById("yRight2").setAttribute('value',Math.trunc(dato2.y*(imageHeightOriginal/rect.height)));
          document.getElementById("wRight2").setAttribute('value',Math.trunc(dato2.width*(imageWidthOriginal/rect.width)));
          document.getElementById("hRight2").setAttribute('value',Math.trunc(dato2.height*(imageHeightOriginal/rect.height)));
          
           }
    }
    });

    canvas.addEventListener('mouseup', function(e) {
      if(selectOneROI==true){ 
        if (e.button === 0){
          isDragging = false;
        }
      }
      if(selectTwoROI==true){ 
        if (e.button === 0){
          isDragging2 = false;
        }
      }
    });

    function draw() {
      img.src = document.getElementById("urlRight").value;
      img.onload = function() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      var scaledWidth = originalWidth * zoomFactor;
      var scaledHeight = originalHeight * zoomFactor;
      var dx = (canvas.width - scaledWidth) / 2 - offsetX;
      var dy = (canvas.height - scaledHeight) / 2 - offsetY;
      ctx.drawImage(img, dx, dy, scaledWidth, scaledHeight);
      ctx.fillStyle = '#212529';
      // Dibujar el borde superior
      //ctx.fillRect(0, 0, canvas.width, 30);
      // Dibujar el borde derecho
      //ctx.fillRect(canvas.width - 30, 0, 30, canvas.height);
      // Dibujar el borde inferior
      //ctx.fillRect(0, canvas.height - 30, canvas.width, 30);
      // Dibujar el borde izquierdo
      //ctx.fillRect(0, 0, 30, canvas.height);
      if (selection) {
        var x = selection.x ;;
        var y = selection.y ;
        var width = selection.width;
        var height = selection.height;
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, width, height);
      }
    }
  }
  
  function draw2() {
      img.src = document.getElementById("urlRight").value;
      img.onload = function() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      var scaledWidth = originalWidth * zoomFactor;
      var scaledHeight = originalHeight * zoomFactor;
      var dx = (canvas.width - scaledWidth) / 2 - offsetX;
      var dy = (canvas.height - scaledHeight) / 2 - offsetY;
      ctx.drawImage(img, dx, dy, scaledWidth, scaledHeight);
  
      if (selection2) {
        var x = selection.x ;
        var y = selection.y ;
        var width = selection.width;
        var height = selection.height;
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, width, height);
         x = selection2.x ;
         y = selection2.y ;
         width = selection2.width;
         height = selection2.height;
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, width, height);
      }
    }
  }

function init() {
  originalWidth = 900;
  originalHeight = 675;
  zoomFit();
}
function zoomFit() {
  draw();
}

canvas.addEventListener('wheel', function(e) {
                
  if (e.deltaY > 0) {
      //zoomLevel -= zoomStep;
      if(zoomFactor>1){
          zoomFactor /= 1.1;
          zoonCounter -=1;
          draw();
          var scaledWidth = originalWidth * zoomFactor;
          var scaledHeight = originalHeight * zoomFactor;
          console.log(zoomFactor)
      }  
  } else {
      //zoomLevel += zoomStep;
      if(zoomFactor<=3.5){
          zoomFactor *= 1.1;
          zoonCounter +=1;
          draw();
          var scaledWidth = originalWidth * zoomFactor;
          var scaledHeight = originalHeight * zoomFactor;
          console.log(zoomFactor)
      }
  }
});

function zoomIn() {
  if(zoomFactor<=3.5){
    zoomFactor *= 1.1;
    zoonCounter +=1;
    draw();
    var scaledWidth = originalWidth * zoomFactor;
    var scaledHeight = originalHeight * zoomFactor;
    console.log(zoomFactor)
  }
}

function zoomOut() {
  if(zoomFactor>1){
    zoomFactor /= 1.1;
    zoonCounter -=1;
    draw();
    var scaledWidth = originalWidth * zoomFactor;
    var scaledHeight = originalHeight * zoomFactor;
    console.log(zoomFactor)
  }
}

function movUp() {
    if(offsetY>=-zoonCounter*20){
        offsetY -= 10;
        console.log("zoomFactor: "+zoomFactor+"zonnCounter: "+zoonCounter+" offsetY: "+offsetY   )
        draw()
    }
}

function movDown() {
    if(offsetY<=zoonCounter*20){
        offsetY += 10;
        console.log("zoomFactor: "+zoomFactor+"zonnCounter: "+zoonCounter+" offsetY: "+offsetY   )
        draw()
    }
}

function movRight() {
    if(offsetX<=zoonCounter*40){
        offsetX += 10;
        console.log("zoomFactor: "+zoomFactor+"zonnCounter: "+zoonCounter+" offsetX: "+offsetX   )
        draw()
    }
}

function movLeft() {
    if(offsetX>=-zoonCounter*40){
        offsetX -= 10;
        console.log("zoomFactor: "+zoomFactor+"zonnCounter: "+zoonCounter+" offsetX: "+offsetX   )
        draw()
    }
}

function resetZoom() {
    zoomFactor = 1;
    offsetX= 0;
    offsetY=0;
    zoonCounter=0;
    draw();
  }

init();