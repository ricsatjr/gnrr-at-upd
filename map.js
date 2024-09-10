document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([14.6554901, 121.0651596], 15);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    fetch('map.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        var geojsonLayer = L.geoJSON(geojsonData, {
            filter: function(feature) {
                // Only include features that are not points
                return feature.geometry.type !== "Point";
            },
            style: function(feature) {
                return {
                    color: "blue",        // Outline color
                    fillColor: "blue",    // Fill color
                    weight: 4,            // Outline weight
                    opacity: 0.5,           // Outline opacity
                    fillOpacity: 0.25      // Fill opacity
                };
            },
            onEachFeature: function(feature, layer) {
                if (feature.properties && feature.properties.name) {
                    layer.bindPopup(feature.properties.name);
                }
            }
        }).addTo(map);

        // Fit map to GeoJSON bounds
        map.fitBounds(geojsonLayer.getBounds());
        
        console.log("GeoJSON layer added to map");
    })
    .catch(error => console.error('Error loading GeoJSON:', error));
});
