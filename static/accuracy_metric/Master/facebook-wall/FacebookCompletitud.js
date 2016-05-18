


        document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("facebook-wall");
        window.setTimeout(function() {
        console.log(element);
        var list = [];
        //los linkados los saco como si fueran "normales" para poder comparar
        for (var i=0;i<element.events.length;i++){
          list.push(element.events[i]);
          if (element.events[i].linked){
            list.push(element.events[i].linked);
          }
        };
        console.log(list.length)

        var shaObj = new jsSHA("SHA-1", "TEXT");
        
        for (var i = 0; i<list.length;i++){
          console.log(i)
          var id= list[i].id
          var user= list[i].from.name
          console.log(user)
          if(list[i].description){
            shaObj.update(list[i].description);
            var hash = shaObj.getHash("HEX");
            var texto=hash
        }
          else{
            if(list[i].message){
            shaObj.update(list[i].message);
            var hash = shaObj.getHash("HEX");
            var texto=hash  
          }
        }
          if(list[i].picture){
            shaObj.update(list[i].picture);
            var hash = shaObj.getHash("HEX"); 
            var image=hash;
          }

          var diccionario = {
            'user': user,
            'i': i,
            'texto':texto,
            'image':image
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("master",{'value':dicc_string});
          }
      }, 5000);
      });