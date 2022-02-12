import os
from pathlib import Path
import matplotlib.pyplot as plt
from rasterio import plot
import rasterio
import geopandas
import pandas as pd
import numpy as np
from rasterio.mask import mask





def read_files(base_dir, file_extensions=['.tif', '.shp']):
    """

    """
    base_dir = Path(base_dir)
    path_files = []
    for elem in os.listdir(base_dir):
        if os.path.isdir(base_dir /elem):
            for x in os.listdir(base_dir / elem):
                if (base_dir / elem / x).suffix in file_extensions:
                    path_files.append(base_dir / elem / x)
        elif  (base_dir / elem).suffix in file_extensions:
            path_files.append(base_dir / elem)
    path_files.sort()
    return path_files



def GeoPlot(vector, raster):
    fig, ax = plt.subplots(figsize = (10,10))
    
    for indx in raster.index:
        my_raster = rasterio.open(raster.loc[indx]["path"])
        
        plot.show(my_raster, ax = ax, cmap = raster.loc[indx]["color"])

    
    for indx in vector.index:
        my_vector = geopandas.read_file(vector.loc[indx]["path"])


        my_vector.plot(ax = ax)


def SamplingValuesRaster(agent, raster):

    agent_copy = agent.copy()
    for indx in raster.index:
        values = []
        my_raster = rasterio.open(raster.loc[indx]["path"])
        for i in range (0, len(agent)):
            for val in my_raster.sample([(agent.geometry.x[i], agent.geometry.y[i])]): 
                values.append(float(val))
        agent_copy[raster.loc[indx]["name"]] = np.array(values)
    return agent_copy



def Zonal_stats(vector, raster, buffer_size=0.1):
    zonal_stats_list = []
    vector_func = vector.copy()
    vector_func["buffer"] = vector_func.buffer(buffer_size)
    for n in range(0, len(vector_func)):
        selected_site = vector_func.iloc[n:n+1]
        out_img, _ = mask(raster, selected_site["buffer"], crop=True, filled=False)
        # statistics ADD MORE?
        img_mean = np.mean(out_img)
        img_median = np.median(out_img)
        img_std = np.std(out_img)
        img_max = np.max(out_img)
        img_min = np.mean(out_img)
        

        zonal_stats_list.append((img_mean, img_median, img_std, img_max, img_min))
        zonal_df = pd.DataFrame(zonal_stats_list, columns=("mean", "median", "std", "max", "min"))

        zonal_stats_df = vector_func.join(zonal_df)

        
    return zonal_stats_df

