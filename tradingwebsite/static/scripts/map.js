APIToken = 'pk.eyJ1IjoiY2F0bmlwbWFzdGVycmFjZSIsImEiOiJjazVuemY3Y2sxYm9mM21xazRtNW9wMGY4In0.DNyNPfASNJAKCUBArIZkSg';
mapboxgl.accessToken = APIToken;

console.log("code is updated");

function httpGetAsync(theUrl, callback){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

function createMap(postcode, map_id){
    
    var postcodeURL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+encodeURI(postcode)+".json?access_token="+encodeURI(APIToken);
    console.log(postcodeURL)
    httpGetAsync(postcodeURL, response => {
        var lnglat = JSON.parse(response).features[0].center;
        var map = new mapboxgl.Map({
            container: map_id,
            style: 'mapbox://styles/mapbox/streets-v11'
        });
    });
}