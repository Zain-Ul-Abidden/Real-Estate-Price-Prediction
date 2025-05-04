
window.onload = onPageLoad;

function getBathValue()  {
    let uiBathRooms = document.getElementsByName("uiBathrooms");
    console.log(uiBathRooms);
    for (var i in uiBathRooms) { 
        if (uiBathRooms[i].checked) { 
            return parseInt(i) + 1;
        }
    }
    return -1;
}

function getBHKValue() {
    let uiBHK = document.getElementsByName("uiBHK");
    console.log(uiBHK);
    for (var i in uiBHK) { 
        if (uiBHK[i].checked) { 
            return parseInt(i) + 1;
        }
    }
    return -1;
}

function onClickedEstimatePrice()  { 
    console.log("Estimate price button clicked");
    let sqft = document.getElementById("uiSqft").value;
    let bhk = getBHKValue();
    let bathrooms = getBathValue();
    let location = document.getElementById("uiLocations").value;

    const url = "http://127.0.0.1:5000/predict_home_price" ; 
    $.post (url, { 
        total_sqft: parseFloat(sqft),
        bhk: bhk,
        bath: bathrooms,
        location: location
    }, function(data, status) { 
        console.log(data);
        document.getElementById("uiEstimatedPrice").innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
        console.log(status);
    });
}

function onPageLoad()  { 
    console.log("document loaded");
    const locationUrl = "http://127.0.0.1:5000/get_location_names" ;
    $.get(locationUrl, (data , status) => {
        console.log("got respponse");
        if (data) { 
            let locations = data.locations;
            let uiLocation = document.getElementById("uiLocations");
            $("#uiLocations").empty();
            for (var  i in locations) { 
                let opt = new Option(locations[i]);
                $("#uiLocations").append(opt);

            }
        }

    }) ;
}