document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('delete_map').setView([40.09, -100.09], 4.5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© united states ONLY'
    }).addTo(map);
    var citiesCoordinates = JSON.parse(document.getElementById('cities-coordinates').textContent);

    function createForm(city_data, city_unique_id) {
        var formContainer = document.getElementById('city-form-container');
        formContainer.innerHTML = '';

        var form = document.createElement('form');
        form.id = 'city-form';
        form.classList.add('container');

        var formRow = document.createElement('div');
        formRow.classList.add('form-row');

        var cityCol = document.createElement('div');
        cityCol.classList.add('col-md-8', 'mb-1');

        var cityLabel = document.createElement('label');
        cityLabel.setAttribute('for', 'city');
        cityLabel.textContent = 'City';

        var cityInput = document.createElement('input');
        cityInput.type = 'text';
        cityInput.classList.add('form-control');
        cityInput.name = 'city';
        cityInput.value = city_data["city"];
        cityInput.required = true;
        cityInput.readOnly = true;

        cityCol.appendChild(cityLabel);
        cityCol.appendChild(cityInput);

        var idCol = document.createElement('div');
        idCol.classList.add('col-md-8', 'mb-4');

        var idLabel = document.createElement('label');
        idLabel.setAttribute('for', 'id');
        idLabel.textContent = 'ID';

        var idInput = document.createElement('input');
        idInput.type = 'text';
        idInput.classList.add('form-control');
        idInput.name = 'id';
        idInput.value = city_unique_id;
        idInput.readOnly = true;

        idCol.appendChild(idLabel);
        idCol.appendChild(idInput);

        var deleteCol = document.createElement('div');
        deleteCol.classList.add('col-md-8', 'mb-2');

        var deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.classList.add('btn', 'btn-danger', 'form-control');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', function () {
            deleteCity(city_data, city_unique_id);
        });

        deleteCol.appendChild(deleteButton);

        formRow.appendChild(cityCol);
        formRow.appendChild(idCol);
        formRow.appendChild(deleteCol);

        form.appendChild(formRow);

        formContainer.appendChild(form);
        }

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
                            createForm(city_data, city_unique_id);
                        };
                    } catch (error) {
                        console.error('Error fetching temperature data for city ' + city_data["city"] + ':', error);
                    }
                });
            })(city_data, city_unique_id);
        }
    }

    addMarkers();
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

function deleteCity(city_data, city_unique_id) {
    // Function to get the CSRF token from cookies
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }

    // Get the CSRF token
    const csrfToken = getCSRFToken();

    var raw = "";

    // Include the CSRF token in the headers only if it's available
    var requestOptions = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: raw,
        redirect: 'follow'
    };

    // Add the CSRF token to headers if available
    if (csrfToken) {
        requestOptions.headers['X-CSRFToken'] = csrfToken;
    }

    fetch(`http://127.0.0.1:8000/geo_django_drf/delete-point/${city_unique_id}/`, requestOptions)
        .then(response => {
            if (response.ok) {
                window.location.href = "/geo_django_map";
            } else {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        })
        .catch(error => {
            console.log('Error:', error.message);
        });
}


