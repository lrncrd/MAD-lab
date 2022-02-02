# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 21:01:45 2021

@author: andre
"""
import geopandas as gpd
import rasterio as rio
from rasterio.plot import plotting_extent
import matplotlib.pyplot as plt
import matplotlib as mpl
#import earthpy as ep

fake_site_path = r'D:/GDrive/adr-data/02_01-software_PROVE/python/geo/shape/fakesite_01.shp'
dem_path = r'D:/GoogleDrive/adr_CNR/progetto_terramare/GIS/dtm_srtm_90.tif'

fake_site = gpd.read_file(fake_site_path)

# with rio.open(dem_path) as dem_src:
#     dem_data = dem_src.read()

dem_src=rio.open(dem_path)


for i in range (0, len(fake_site)):
    coord_x = fake_site.at[i,'geometry'].x
    coord_y = fake_site.at[i,'geometry'].y
    raster_pixel = dem_src.sample([(coord_x, coord_y)])
    print(list(raster_pixel)[0])
    





#dem_plot_extent = plotting_extent(dem_src)


    

# f, ax = plt.subplots()
# ep.plot_bands(dem_data)

# fake_site.plot(ax=ax)
# plt.show