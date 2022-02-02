# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:51:47 2021

@author: andre
"""
from osgeo import gdal
from osgeo import ogr
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

#shape with points position
myShapefile =  r"D:/GDrive/adr-data/02_01-software_PROVE/python/geo/shape/fakesite_01.shp"

#raster position
filename = 'D:/GoogleDrive/adr_CNR/progetto_terramare/GIS/dtm_srtm_90.tif'

#opening shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')
dataSource = driver.Open(myShapefile, 0)
layer = dataSource.GetLayer()

#get lat/long of the first element of the shapefile
firstFeature = layer[0]
firstGeom = firstFeature.geometry()


bufferDistance = 500
poly = firstFeature.Buffer(firstGeom)

poly.plot()

# geomFirstFeature = firstFeature.geometry()
# coordinates = (geomFirstFeature.GetX(), geomFirstFeature.GetY())

#opening raster file
gdal_data = gdal.Open(filename)

#if we want to remove NoDataValues
# gdal_band = gdal_data.GetRasterBand(1)
# nodataval = gdal_band.GetNoDataValue()

#read rasterFile as numpyArray
data_array = gdal_data.ReadAsArray().astype(float)






#plot rasterFile
# plt.figure(figsize = (8, 8))
# plt.axis("on")
# img = plt.imshow(data_array, cmap = "viridis")

