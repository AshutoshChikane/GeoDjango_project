document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('edit_map').setView([40.09, -100.09], 4.5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© united states ONLY'
    }).addTo(map);
    var citiesCoordinates = JSON.parse(document.getElementById('cities-coordinates').textContent);



    async function addMarkers() {
        for (var i = 0; i < citiesCoordinates.length; i++) {
            var city_unique_id = Object.keys(citiesCoordinates[i])[0];
            var city_data = citiesCoordinates[i][city_unique_id];

            (function (city_data, city_unique_id) {
                var marker = L.marker(city_data["lat_lng"]).addTo(map);

                marker.on('click', async function (e) {
                    try {
                        var temperature = await fetchData(city_data);
                        if (temperature !== false) {
                            const city_property = temperature.properties.periods[0];
                            var formContainer = document.getElementById('city-form-container');
                            formContainer.innerHTML = '';
                            var popupContent = '<b>id:</b>' + city_unique_id +
                                '<br><b>City: </b>' + city_data["city"] +
                                '<br><b>Temperature: </b>' + city_property["temperature"] +
                                '<br><b>Humidity: </b>' + city_property["relativeHumidity"]["value"];

                            e.target.bindPopup(popupContent).openPopup();
                        };
                    } catch (error) {
                        console.error('Error fetching temperature data for city ' + city_data["city"] + ':', error);
                    }
                });
            })(city_data, city_unique_id);
        }
    }
    var city_id = Object.keys(citiesCoordinates[0])[0]
    addMarkers();
    var currentMarker = null;
    function onMapClick(e) {
    if (currentMarker) {
      map.removeLayer(currentMarker);
    }
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;
    currentMarker = L.marker([lat,lng]).addTo(map);
    console.log(city_id)
    createForm(lat, lng, city_id);

    }
    map.on('click', function(e) {
    onMapClick(e, city_id);
    });
    });

function fetchData(city_data) {
    const baseUrl = "https://api.weather.gov/gridpoints";
    const apiUrl = `${baseUrl}/${city_data["gridId"]}/${city_data["gridX"]},${city_data["gridY"]}/forecast`;
    return fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                return false
            }
            return response.json();
        })
        .catch(error => {
            throw error;
        });
}

function editCity(latitude,longitude,city_id) {
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }

    const csrfToken = getCSRFToken();

    var raw = JSON.stringify({
      "longitude": longitude,
      "latitude": latitude
    });

    var requestOptions = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: raw,
        redirect: 'follow'
    };

    if (csrfToken) {
        requestOptions.headers['X-CSRFToken'] = csrfToken;
    }

    fetch(`http://127.0.0.1:8000/geo_django_drf/update-point/${city_id}/`, requestOptions)
        .then(response => {
            if (response.ok) {
                window.location.href = "/geo_django_map";
                alert("updated location successfully")
            } else {
                throw new Error(`HTTP error! Status: ${response.text}`);
            }
        })
        .then(data => {
            console.log(data.detail);
          })
        .catch(error => {
            console.log('Error:', error.message);
            var formContainer = document.getElementById('city-form-container');
            formContainer.innerHTML = '<h3>We are only present at United states please Mark Again</h3>'
        });
}


function createForm(latitude, longitude, city_id) {
    var formContainer = document.getElementById('city-form-container');
    formContainer.innerHTML = '';

    var form = document.createElement('form');
    form.id = 'city-form';
    form.classList.add('container');

    var formRow = document.createElement('div');
    formRow.classList.add('form-row');

    // Latitude Input
    var latitudeCol = document.createElement('div');
    latitudeCol.classList.add('col-md-12', 'mb-1');

    var latitudeLabel = document.createElement('label');
    latitudeLabel.setAttribute('for', 'latitude');
    latitudeLabel.textContent = 'Latitude';

    var latitudeInput = document.createElement('input');
    latitudeInput.type = 'text';
    latitudeInput.classList.add('form-control');
    latitudeInput.name = 'latitude';
    latitudeInput.value = latitude;
    latitudeInput.required = true;
    latitudeInput.readOnly = true;

    latitudeCol.appendChild(latitudeLabel);
    latitudeCol.appendChild(latitudeInput);

    var longitudeCol = document.createElement('div');
    longitudeCol.classList.add('col-md-12', 'mb-4');

    var longitudeLabel = document.createElement('label');
    longitudeLabel.setAttribute('for', 'longitude');
    longitudeLabel.textContent = 'Longitude';

    var longitudeInput = document.createElement('input');
    longitudeInput.type = 'text';
    longitudeInput.classList.add('form-control');
    longitudeInput.name = 'longitude';
    longitudeInput.value = longitude;
    longitudeInput.readOnly = true;

    longitudeCol.appendChild(longitudeLabel);
    longitudeCol.appendChild(longitudeInput);

    var editCol = document.createElement('div');
    editCol.classList.add('col-md-12', 'mb-2');

    var editButton = document.createElement('button');
    editButton.type = 'button';
    editButton.classList.add('btn', 'btn-success', 'form-control');
    editButton.textContent = 'Update Location';
    editButton.addEventListener('click', function () {
        editCity(latitude, longitude, city_id);
    });

    editCol.appendChild(editButton);

    formRow.appendChild(latitudeCol);
    formRow.appendChild(longitudeCol);
    formRow.appendChild(editCol);

    form.appendChild(formRow);

    formContainer.appendChild(form);
}
