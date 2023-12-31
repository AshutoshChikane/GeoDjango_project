document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([40.09, -100.09], 4.5);

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
