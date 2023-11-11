document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([37.09, -95.09], 4);  // Centered on the United States

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    var citiesCoordinates = JSON.parse(document.getElementById('cities-coordinates').textContent);

    async function addMarkers() {
        for (var i = 0; i < citiesCoordinates.length; i++) {
            var city_unique_id = Object.keys(citiesCoordinates[i])[0];
            var city_data = citiesCoordinates[i][city_unique_id];

            try {
                var temperature = await fetchData(city_data["temperature_url"]);
                const city_property =  temperature.properties.periods[0];
                console.log(city_property);

                var marker = L.marker(city_data["lat_lng"]).addTo(map);

                var popupContent = '<b>id:</b>' + city_unique_id +
                    '<br><b>Name:</b>' + city_data["city"] +
                    '<br><b>Temperature:</b>' + city_property["temperature"] +
                    '<br><b>Humidity:</b>' + city_property["relativeHumidity"]["value"] ;
                marker.bindPopup(popupContent);
            } catch (error) {
                console.error('Error fetching temperature data for city '+city_data["city"]+':', error);
            }
        }

    }
    addMarkers();
});

function fetchData(url) {
  // Define the API URL
  const apiUrl = url;

  // Make a GET request to the API
  return fetch(apiUrl)
    .then(response => {
      // Check if the response status is OK (200)
      if (!response.ok) {
        throw new Error('HTTP error! Status: ${response.status}');
      }

      // Parse the JSON response
      return response.json();
    })
    .catch(error => {
        console.log(response)
        console.error('Error fetching temperature data for city', error);
    });
}
