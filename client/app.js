window.onload = onPageLoad;

function getBathValue() {
    let uiBathRooms = document.getElementsByName("uiBathrooms");
    for (let i = 0; i < uiBathRooms.length; i++) {
        if (uiBathRooms[i].checked) {
            return parseInt(uiBathRooms[i].value);
        }
    }
    return -1;
}

function getBHKValue() {
    let uiBHK = document.getElementsByName("uiBHK");
    for (let i = 0; i < uiBHK.length; i++) {
        if (uiBHK[i].checked) {
            return parseInt(uiBHK[i].value);
        }
    }
    return -1;
}

function onClickedEstimatePrice() {
    let sqft = document.getElementById("uiSqft").value;
    let bhk = getBHKValue();
    let bathrooms = getBathValue();
    let location = document.getElementById("uiLocations").value;

    if (!location || bhk === -1 || bathrooms === -1 || !sqft) {
        alert("Please fill all fields correctly");
        return;
    }

    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("uiEstimatedPrice");

    resultDiv.classList.add("hidden");
    loader.classList.remove("hidden");

    fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            total_sqft: parseFloat(sqft),
            bhk: bhk,
            bath: bathrooms,
            location: location
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Prediction failed");
        }
        return response.json();
    })
    .then(data => {
        loader.classList.add("hidden");
        resultDiv.innerHTML = `₹ ${data.estimated_price} Lakh`;
        resultDiv.classList.remove("hidden");
    })
    .catch(error => {
        loader.classList.add("hidden");
        alert("Error while fetching prediction");
        console.error(error);
    });
}

function onPageLoad() {
    fetch("http://127.0.0.1:8000/locations")
        .then(response => response.json())
        .then(data => {
            let uiLocation = document.getElementById("uiLocations");
            uiLocation.innerHTML = "";

            data.locations.forEach(location => {
                let opt = document.createElement("option");
                opt.value = location;
                opt.text = location;
                uiLocation.appendChild(opt);
            });
        })
        .catch(error => {
            console.error("Error loading locations:", error);
        });
}
