## Author: The Leopards (Samantha Krawczyk, Georgios Anastasiou)
## 22 January 2016
## Creating shapefile with locations found in a txt file

import os
import requests
from osgeo import ogr, osr

os.getcwd()

## create your output directory and set it as your working directory
os.chdir('assignment15')

txt_file = open("Cities.txt", "r")
CitiesList = txt_file.read().split(',')

## Is the ESRI Shapefile driver available?
driverName = "ESRI Shapefile"
driver = ogr.GetDriverByName(driverName)
if driver is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName


## Set the name of the layer and the shapfile
fn = "locations.shp"
layername = "cities"

## Create shape file
ds = driver.CreateDataSource(fn)

## Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

## Create Layer
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)

for city in CitiesList:
    ## Get coordinates
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': city}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']
    location['lat'], location['lng']

    ## Create a point
    cityPoint = ogr.Geometry(ogr.wkbPoint)

    ## SetPoint(self, int point, double x, double y, double z = 0)
    cityPoint.SetPoint(0, location['lng'], location['lat'])

    ## Feature is defined from properties of the layer
    layerDefinition = layer.GetLayerDefn()
    feature = ogr.Feature(layerDefinition)

    ## Lets add the points to the feature
    feature.SetGeometry(cityPoint)

    ## Store the feature in a layer
    layer.CreateFeature(feature)

ds.Destroy()










