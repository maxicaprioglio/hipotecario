document.addEventListener("DOMContentLoaded", function () {
  // envio de formulario
  const formulario = document.getElementById("formulario");
  const btnSimular = document.getElementById("btn-simular");
  const spinner = document.getElementById("spinner");
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  // funcion de limpieza de errores
  function limpiarErrores() {
    const idsErrores = ["nombre",
      "edad",
      "email",
      "celular",
      "tipo_empleo",
      "antiguedad_laboral",
      "bruto",
      "propiedad",
      "ahorros",
      "plazo"];
    
    idsErrores.forEach(id => {
      document.getElementById("error_" + id).innerText = "";
    });
  }

  // limpieza de cotizaciones previas
  function limpiarCotizaciones() {
    const idsCotizaciones = ["bruto",
          "propiedad",
          "ahorros"];
    idsCotizaciones.forEach(id => {
      document.getElementById("equivalente_" + id).innerText = "";
    });
  }

  // Agregar evento de submit al formulario
  formulario.addEventListener("submit", function (event) {
    event.preventDefault();
    // Activar spinner y deshabilitar botón
    spinner.style.display = "inline-block";
    btnSimular.disabled = true;

    // Validación de campos
    const formData = new FormData(formulario);
    fetch("/", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrfToken,
      }
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.mensaje_exito) {
          // dejar el formulario en blanco
          formulario.reset();

          // Limpiar mensajes previos
          limpiarErrores();
          limpiarCotizaciones();
          document.getElementById("error_general").innerText = "";
          document.getElementById("mensaje_exito").innerText = "";

          // Mostrar mensaje de éxito
          document.getElementById("mensaje_exito").innerText = "Formulario enviado correctamente.";
          // Mostrar mensaje de error de no se pudo enviar el mail
          if (data.error) {
            document.getElementById("error_general").innerText = "No se pudo enviar el mail. Por favor, intente nuevamente más tarde o revise su email este bien.";
          }

          // Mostrar informe de cotización
          document.getElementById("informe").style.display = "block";
          document.getElementById("informe-cliente").innerText = data.informe.cliente;
          document.getElementById("informe-importe").innerText = `$ ${data.informe.importe}.-`;
          document.getElementById("informe-plazo").innerText = `${data.informe.plazo} cuotas`;
          document.getElementById("informe-cuotas").innerText = `$ ${data.informe.cuotas}.-`;
        } else {
            // Limpiar mensajes previos
            limpiarErrores();

            //error_general
            if (data.error) {
              document.getElementById("error_general").innerText = "No se pudo guardar la consulta, inténtalo más tarde.";
            }
            
            // Mostrar mensaje de error
            for (let campo in data.errors) {
                const errorDiv = document.getElementById(`error_${campo}`);
                if (errorDiv) {
                  errorDiv.textContent = data.errors[campo][0];
                }
            }
        }
    })
    .catch((error) => {
      document.getElementById("error_general").innerText = "Error importante, por favor intenta nuevamente más tarde.";
    })
    .finally(() => {
      // Ocultar spinner y restaurar texto del botón
      spinner.style.display = "none";
      btnSimular.disabled = false;

      // Hacer scroll hacia el informe
      const informe = document.getElementById("informe");
      if (informe) {
        informe.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Obtener cotización
  const campos = ["bruto", "propiedad", "ahorros"];
  let valorDolar = null;

  fetch("/api/cotizacion/")
    .then((response) => response.json())
    .then((data) => {
      if (!data.error) {
        valorDolar = data.valor;
      }
    });

  campos.forEach((id) => {
    // Crear un div para mostrar la información debajo del campo
    const campo = document.getElementById(id);
    const divPadre = campo.closest(".col-12"); 
    const infoDiv = document.createElement("div");
    infoDiv.classList.add("form-text", "text-success", "mt-1");
    infoDiv.id = `equivalente_${id}`;
    divPadre.appendChild(infoDiv); 

    // Agregar el evento de input para actualizar la información
    campo.addEventListener("input", function () {
      const valor = parseFloat(campo.value);
      if (!isNaN(valor) && valorDolar) {
        const dolares = (valor / valorDolar).toFixed(2);
        infoDiv.textContent = `Este importe equivale a ${dolares} dólares bajo la cotización del dólar oficial del día ($${valorDolar}).`;
      } else {
        infoDiv.textContent = "";
      }
    });
  });
});
