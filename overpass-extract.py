import csv
import requests
import json
import sys
import traceback
import os

def create_overpass_query(csv_file_path):
    feat_types = []
    ids = []
    
    print(f"Opening CSV file: {csv_file_path}")
    with open(csv_file_path, 'r') as csvfile:
        print(f"First few lines of the CSV file:")
        for i, line in enumerate(csvfile):
            print(line.strip())
            if i >= 5:  # Print first 5 lines
                break
        csvfile.seek(0)  # Reset file pointer to the beginning
        
        csv_reader = csv.DictReader(csvfile)
        print(f"CSV headers: {csv_reader.fieldnames}")
        
        for row in csv_reader:
            osmid = row['osmid']
            print(f"Processing row: {row}")
            id_parts = osmid.split('/')
            if len(id_parts) != 2:
                print(f"Warning: Unexpected OSM ID format: {osmid}")
                continue
            ids.append(id_parts[1])  # Extract the numeric ID
            feat_types.append(id_parts[0])  # Extract the feature type ID
    
    # Create the Overpass query
    query = "[out:json];\n(\n"
    for f in range(len(ids)):
        query += f"  {feat_types[f]}(id:{ids[f]});\n"
    query += ");\nout geom;"
    
    print(f"Generated query:\n{query}")
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
    
    try:
        # Create the Overpass query
        query = create_overpass_query(csv_file_path)
        
        # Set up the request
        overpass_url = "https://overpass-api.de/api/interpreter"
        print(f"Sending request to {overpass_url}")
        response = requests.get(overpass_url, params={'data': query})
        response.raise_for_status()  # This will raise an exception for HTTP errors
        
        print(f"Request status code: {response.status_code}")
        
        # Parse the JSON response
        osm_data = response.json()
        
        # Convert OSM JSON to GeoJSON
        geojson_data = osm_to_geojson(osm_data)
        
        # Save the data as GeoJSON
        with open(output_file_path, 'w') as f:
            json.dump(geojson_data, f, indent=2)
        
        print(f"GeoJSON data saved to {output_file_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        raise  # Re-raise the exception to ensure the GitHub Action fails if there's an error

# Main execution
if __name__ == "__main__":
    csv_file_path = 'buildings.csv'
    output_file_path = 'buildings.geojson'
    
    query_overpass_and_save_geojson(csv_file_path, output_file_path)
    
    print("Current working directory:", os.getcwd())
    print("Files in current directory:", os.listdir())
    if os.path.exists('buildings.geojson'):
        print("buildings.geojson file size:", os.path.getsize('buildings.geojson'))
    else:
        print("buildings.geojson not found in the current directory")
