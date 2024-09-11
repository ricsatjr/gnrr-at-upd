This repo hosts the overpass turbo query and results for buildings with gender-neutral restrooms in the University of the Philippines Diliiman. 

Identify and list the buildings that you want to show on the map. 
1. Go to https://www.openstreetmap.org/#map=15/14.65480/121.06740&layers=P
2. Click the "Query features" button on the right.
3. Click on a target building.
4. On the Query Features pane appearing on the left of the screen, hover over the links that appear, and take note of the link which highlights your target building on the map. Click that link and get the feature type (node/way/relations), feature name, and the unique numerical OSM ID of that feature. These info are found on the left pane of the page.  For example, this url (https://www.openstreetmap.org/way/258074039) will return a page where the left pane shows a main text: " Way: Abelardo Hall Auditorium (258074039)". 
5. Input this info on the csv file (e.g., test_buildings.csv). Commit (save) the changes to that file.

Generate the GIS file for your collection of buildings. 
1. Construct the query text that you will use (e.g., test_overpass_query.txt) based on the csv file (e.g., test_buildings.csv). Copy the text to the clipboard. Commit the changes to the query file.
2. Open https://overpass-turbo.eu/# in a browser
3. Paste the query text onto the query pane, and then click the "Run" button.
4. Verify if the results shown on the map are consistent with your input.
5. Click "Export" and the "copy" button corresponding to the GeoJSON data format. 
6. Paste the GeoJSON data onto the geojson file (e.g., test_overpass_query_result.geojson)
7. Commit the changes to the results file.

The "index.html" is a sample webpage which contains a map defined by the file "map.js", which in turn, uses the "test_overpass_query_result.geojson" as input data.  You can modify the map's layout and input data by modifying "map.js"

The sample webpage maybe accessed via this url:  "https://ricsatjr.github.io/gnrr-at-upd/index.html".  
