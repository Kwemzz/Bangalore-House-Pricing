
function onPageLoad(){
    var url = "http://127.0.0.1:5000/get_location_names";
    $.get(url,function(data, status){
        console.log("got response for get_location_names request");
        if(data){
            var locations = data.locations;
            var ullocation = document.getElementById("ullocation");
            $('ullocation').empty();
            for(var i in location){
                var opt = new Option(locations[i]);
                $('#ullocation').append(opt);
            }
        }
    })
}

window.onload = onPageLoad;