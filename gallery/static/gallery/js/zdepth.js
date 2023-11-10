const resultDiv = document.getElementById('result');
document.getElementById('enviar').addEventListener('click', async function () {
    console.log("spasa por aca");
    //event.preventDefault();
    const urlRight = document.getElementById('urlRight').value;
    const urlLeft = document.getElementById('urlLeft').value;
    const xRight = document.getElementById('xRight').value;
    const yRight = document.getElementById('yRight').value;
    const wRight = document.getElementById('wRight').value;
    const hRight = document.getElementById('hRight').value;
    const lat = document.getElementById('lat').value;
    const lon = document.getElementById('lon').value;
    const lat_next = document.getElementById('lat_next').value;
    const lon_next = document.getElementById('lon_next').value;
    const xRight2 = document.getElementById('xRight2').value;
    const yRight2 = document.getElementById('yRight2').value;
    const wRight2 = document.getElementById('wRight2').value;
    const hRight2 = document.getElementById('hRight2').value;
    const pk = document.getElementById('pk').value;
    const pk2 = document.getElementById('pk2').value;
    const distanceObjects = document.getElementById('distanceObjects').value;
    
    try {
        console.log("xRight2: "+xRight2)
        if(distanceObjects=="false"){   
            console.log("distanceObjects FALSE")
            const response = await fetch(`/zdepth/?urlRight=${urlRight}&urlLeft=${urlLeft}&xRight=${xRight}&yRight=${yRight}&wRight=${wRight}&hRight=${hRight}&lat=${lat}&lon=${lon}&lat_next=${lat_next}&lon_next=${lon_next}&pk=${pk}&pk2=${pk2}`);
            const data = await response.json();
            if (data.zdepth) {
                resultDiv.innerText = `Profundidad desde el centro en Z: ${data.zdepth} / X:${data.x} / Disp:${data.disp}`; 
                document.getElementById("form_latitude").setAttribute('value',`${data.lat_new}`);
                document.getElementById("form_longitude").setAttribute('value',`${data.lon_new}`);
                document.getElementById("form_center_x").setAttribute('value',xRight); 
                document.getElementById("form_center_y").setAttribute('value',yRight); 
                document.getElementById("form_width").setAttribute('value',wRight); 
                document.getElementById("form_height").setAttribute('value',hRight); 
                console.log(data.disp)
                console.log(data.x)
                console.log(data.lat_new)
                console.log(data.lon_new)
            } else {
                resultDiv.innerText = `File not found`;
                console.log("no hay nada")
            }
        } 
        if(distanceObjects=="true"){
            console.log("distanceObjects TRUE")
            const response = await fetch(`/distanceObjects/?urlRight=${urlRight}&urlLeft=${urlLeft}&xRight=${xRight}&yRight=${yRight}&wRight=${wRight}&hRight=${hRight}&xRight2=${xRight2}&yRight2=${yRight2}&wRight2=${wRight2}&hRight2=${hRight2}`);
            const data = await response.json();
            if (data.distance) {
                resultDiv.innerText = `Distancia entre objetos: ${data.distance} `; 
                console.log(data.distance)
            } else {
                resultDiv.innerText = `File not found`;
                console.log("no hay nada")
            }
        }
    } catch (error) {
        console.log("hubo un error");
        resultDiv.innerText = `Error: ${error.message}`;
    }
});