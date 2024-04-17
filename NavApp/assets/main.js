if (locationDetails) {
    init(locationDetails.getLocationId(), locationDetails.getAccessToken());
}

// init("zlaxo0bxzmhqrp9", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2xsZWN0aW9uSWQiOiJfcGJfdXNlcnNfYXV0aF8iLCJleHAiOjE3MTQ1MjgyMzAsImlkIjoiYnAxY3BiNTExdXo5a3VnIiwidHlwZSI6ImF1dGhSZWNvcmQifQ.Qdu--OeT2rIc4-QyK2VUVt-nHcxnvTs-5S5KHbRm0dY").then(r => console.log(r))

async function init(locationId, accessToken) {
    const data = await fetchData(locationId, accessToken);

    console.log(data.center);
    console.log(data.coords);
    displayMap(data.coords, data.center);
}

async function fetchData(locationId, accessToken) {
    const resp = await fetch(`https://api.green-stem.eu/api/collections/locations/records/${locationId}`, {
        headers: {
            "Authorization": accessToken,
        },
    });

    const body = await resp.json();

    const latitudes = body.latitude.latitude;
    const longitudes = body.longitude.longitude;

    const centerLat = latitudes.reduce((acc, curr) => acc + curr) / latitudes.length;
    const centerLon = longitudes.reduce((acc, curr) => acc + curr) / longitudes.length;
    const center = [Number(centerLon), Number(centerLat)];

    const coords = [];

    for (const [i, lat] of latitudes.entries()) {
        coords.push([Number(longitudes[i]), Number(lat)]);
    }

    return {
        coords: coords,
        center: center,
    };
}

function displayMap(coords, center) {
    const map = new maplibregl.Map({
        container: 'map',
        style:
            'https://api.maptiler.com/maps/streets/style.json?key=lY1bvvaxXQRRVYw8tOll',
        center: center,
        zoom: 15
    });

    console.log(coords);

    map.on('load', () => {
        map.addSource('route', {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coords,
                }
            }
        });
        map.addLayer({
            'id': 'route',
            'type': 'line',
            'source': 'route',
            'layout': {
                'line-join': 'round',
                'line-cap': 'round'
            },
            'paint': {
                'line-color': '#888',
                'line-width': 8
            }
        });
    });
}