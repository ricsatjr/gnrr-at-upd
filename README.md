This repo hosts the overpass turbo query and results for buildings with gender-neutral restrooms in the University of the Philippines Diliiman. 

To create a query:
1. Go to https://www.openstreetmap.org/#map=15/14.65480/121.06740&layers=P
2. Click the query features button on the right.
3. Click on a target building, and take note of the building name. Repeat for all target buildings
5. Go to https://overpass-turbo.eu/#
6. type this query statement:

  way["name"~"<building 1 name>|<building 2 name>|<building n name>"]["building"="yes"](14.64566603208577,121.05144023895264,14.663809930484568,121.0786485671997);
  (._;>;);
  out;

7. Replace <building x name> with the actual names of buildings that you noted in step #3.
8. Execute the query
9. Click export --> Data --> Geojson --> Copy. This will copy the geojson file to your clipboard.
10. Open the existing geojson file, clear it, and then paste the updated geojson file from your clipboard.
11. Commit the changes to your geojson file.

Viewing the geojson file in geojson.io:
1. open a web browser
2. type "https://geojson.io/#id=github:ricsatjr/gnrr-at-upd/blob/main/<geojson file>&map" on the address bar.
3. replace <geojson file> with the actual name of the geojson file. 
   
