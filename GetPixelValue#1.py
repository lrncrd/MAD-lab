# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 01:00:08 2021

@author: andre
"""
import os
from osgeo import ogr
from osgeo import gdal
import rasterio
import rasterio.plot
import matplotlib.pyplot as plt
import matplotlib as mpl

#import geopandas as gp

os.environ['PROJ_LIB'] = 'C:/Users/andre/.conda/envs/adr_training/Library/share/proj'
os.environ['GDAL_DATA'] ='C:/Users/andre/.conda/envs/adr_training/Library/share/gdal'



myDem = rasterio.open('D:/GoogleDrive/adr_CNR/progetto_terramare/GIS/dtm_srtm_90.tif')
myShapefile =  r"D:/GDrive/adr-data/02_01-software_PROVE/python/geo/shape/fakesite_01.shp"
driver = ogr.GetDriverByName('ESRI Shapefile')
dataSource = driver.Open(myShapefile, 0)



if dataSource is None:
    print ('Could not open %s' % (myShapefile))
else:
    print ('Opened %s' % (myShapefile))
    layer = dataSource.GetLayer()
    layerDefinition = layer.GetLayerDefn()
    featureCount = layer.GetFeatureCount()
    print ("Number of features in %s: %d" % (os.path.basename(myShapefile),featureCount))
    

#list_field = ['id','nome']
for feature in layer:
    values_list = [feature.GetField(0), feature.GetField(1)] #for j in list_field]
    geom =feature.geometry()
    x_coord = geom.GetX()
    y_coord = geom.GetY()
    raster_value = myDem.sample([(x_coord, y_coord)])
    value = list(raster_value)
    #value = value[0] + 0
   
    print  (value[0])
# plt.imshow(myDem.read(1), cmap='Blues')  
# plt.show(myDem)

# rasterio.plot.show((myDem, 1))
# ax = mpl.pyplot.gca()
# patches = [layer[0]]
# ax.add_collection(mpl.collections.PatchCollection(patches))    





