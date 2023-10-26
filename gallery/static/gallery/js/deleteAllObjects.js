

    function borrarObjetos(boton) {
      var pk= document.getElementById("pk").value;
      var pk2= document.getElementById("pk2").value;
      enviarDatosAlBackend(pk,pk2);
      
    }

    async function enviarDatosAlBackend(pk,pk2) {
   
      try {
        const response = await fetch(`/deleteallobjects/?pk=${pk}&pk2=${pk2}`);
        const data = await response.json();
        
          console.log(data);
      
      } catch (error) {
        console.log(error.message);
      }
      window.location.reload();
      
    }
   