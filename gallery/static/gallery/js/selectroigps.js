var canvas = document.getElementById("canvas");
var canvas2 = document.getElementById("canvas2");
    var ctx = canvas.getContext("2d");
    var ctx2 = canvas2.getContext("2d");
    var img = new Image();
    var img2 = new Image();
    canvas.width = 900;
    canvas2.width = 900;

    img.src= document.getElementById("urlRight").value;
    console.log(img)
    img.onload = function() {
      ctx.drawImage(img, 0, 0);
    };
    img2.src= document.getElementById("urlRight2").value;
    img2.onload = function() {
      ctx2.drawImage(img2, 0, 0);
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
    var imageWidthOriginal=2666;
    var imageHeight=675;
    var imageHeightOriginal=2000;
    var factorX=imageWidth/imageWidthOriginal;
    var factory=imageHeight/imageHeightOriginal;

   
    

    

    canvas.addEventListener('mousedown', function(e) {
    
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
    });

    canvas2.addEventListener('mousedown', function(e) {
    
      if (e.button === 0){
        isDragging2 = true;
        var rect = canvas2.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
 
        originx2=x*(imageWidth/rect.width);
        originy2=y*(imageHeight/rect.height);
        selection2 = { x: originx, y: originy, width: 0, height: 0 };
        dato2={ x: x, y: y, width: 0, height: 0 };
      }
    });

    canvas2.addEventListener('mousemove', function(e) {
       
        if (isDragging2) {
          draw2();
          var rect = canvas2.getBoundingClientRect();
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
      
    
    });

    canvas.addEventListener('mousemove', function(e) {
       
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
    
  
  });

    canvas.addEventListener('mouseup', function(e) {
        if (e.button === 0){
          isDragging = false;
        }
      
      
    });

    canvas2.addEventListener('mouseup', function(e) {
      if (e.button === 0){
        isDragging2 = false;
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
      img2.src = document.getElementById("urlRight2").value;
      img2.onload = function() {
      ctx2.clearRect(0, 0, canvas2.width, canvas2.height);
      var scaledWidth = originalWidth * zoomFactor;
      var scaledHeight = originalHeight * zoomFactor;
      var dx = (canvas2.width - scaledWidth) / 2 - offsetX;
      var dy = (canvas2.height - scaledHeight) / 2 - offsetY;
      ctx2.drawImage(img, dx, dy, scaledWidth, scaledHeight);
  
      if (selection2) {
        var x = selection2.x ;;
        var y = selection2.y ;
        var width = selection2.width;
        var height = selection2.height;
        ctx2.strokeStyle = 'blue';
        ctx2.lineWidth = 2;
        ctx2.strokeRect(x, y, width, height);
      }
    }
  }

function init() {
  originalWidth = 900;
  originalHeight = 675;
  zoomFit();
}
function zoomFit() {
  draw2();
  draw();
}


init();