//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

document.addEventListener('WebComponentsReady', function () {
  //selecccionamos el componente de twitter con el querySelector
  var element = document.querySelector("open-weather");
  window.setTimeout(function () {
    for (var i = 0; i < element.data.length; i++) {
      var city = element.data[i].name;
      var date = element.data[i].current_date;
      var time = element.data[i].current_time;
      var day = element.data[i].day;
      var icon = element.data[i].icon;
      var temp = element.data[i].currentTemp;
      var temp_max = element.data[i].maxTemp;
      var temp_min = element.data[i].minTemp;

      //almaceno todas las variables en un diccionario
      var diccionario = {
        'city': city,
        'fecha': date,
        'hora': time,
        'dia': day,
        'icon': icon,
        'temp': temp,
        'temp_max': temp_max,
        'temp_min': temp_min,
        'i': i
      };
      var dicc_string = JSON.stringify(diccionario);
      //mando a mixpanel los campos recogidos en el diccionario
      mixpanel.track("master", { 'value': dicc_string });
    }
  }, 2000);
});