import csv
import requests
import json

def create_overpass_query(csv_file_path):
    feat_types=[]
    ids = []
    
    # Read the CSV file and extract the way IDs
    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            osmid = row['osmid']
            ids.append(osmid.split('/')[1])  # Extract the numeric ID
            feat_types.append(osmid.split('/')[0]) # Extract the feature type ID
    
    # Create the Overpass query
    query = "[out:json];\n(\n"
    for f in range(len(ids)):
        query += f"  {feat_types[f]}(id:{ids[f]});\n"
    query += ");\nout geom;"
    
    return query

def osm_to_geojson(osm_data):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for element in osm_data['elements']:
        feature = {
            "type": "Feature",
            "properties": {
                "id": element['id'],
                "type": element['type'],
                "tags": element.get('tags', {})
            }
        }
        
        if element['type'] == 'node':
            feature['geometry'] = {
                "type": "Point",
                "coordinates": [element['lon'], element['lat']]
            }
        elif element['type'] == 'way':
            coordinates = [[node['lon'], node['lat']] for node in element['geometry']]
            if coordinates[0] == coordinates[-1] and len(coordinates) > 3:
                feature['geometry'] = {
                    "type": "Polygon",
                    "coordinates": [coordinates]
                }
            else:
                feature['geometry'] = {
                    "type": "LineString",
                    "coordinates": coordinates
                }
        elif element['type'] == 'relation':
            # For simplicity, we'll treat relations as MultiPolygons
            # This is a simplified approach and might need refinement for complex relations
            feature['geometry'] = {
                "type": "MultiPolygon",
                "coordinates": []
            }
            for member in element.get('members', []):
                if member['type'] == 'way' and 'geometry' in member:
                    coords = [[node['lon'], node['lat']] for node in member['geometry']]
                    if coords[0] == coords[-1] and len(coords) > 3:
                        feature['geometry']['coordinates'].append([coords])
        
        geojson['features'].append(feature)
    
    return geojson

def query_overpass_and_save_geojson(csv_file_path, output_file_path):
    print(f"Starting script with CSV file: {csv_file_path}")
    
    # Create the Overpass query
    query = create_overpass_query(csv_file_path)
    print(f"Generated query: {query}")
    
    # Set up the request
    overpass_url = "https://overpass-api.de/api/interpreter"
    print(f"Sending request to {overpass_url}")
    try:
        response = requests.get(overpass_url, params={'data': query})
        response.raise_for_status()  # This will raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return

    print(f"Request status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful")
        try:
            # Parse the JSON response
            osm_data = response.json()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Response content: {response.text[:1000]}")  # Print first 1000 characters of response
            return
        
        # Convert OSM JSON to GeoJSON
        geojson_data = osm_to_geojson(osm_data)
        
        # Save the data as GeoJSON
        try:
            with open(output_file_path, 'w') as f:
                json.dump(geojson_data, f, indent=2)
            print(f"GeoJSON data saved to {output_file_path}")
        except IOError as e:
            print(f"Error writing to file: {e}")
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        print(f"Response content: {response.text[:1000]}")  # Print first 1000 characters of response

# Usage
csv_file_path = 'buildings.csv'
output_file_path = 'buildings.geojson'
print("Script started")
query_overpass_and_save_geojson(csv_file_path, output_file_path)
print("Script finished")
