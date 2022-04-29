import os
from pathlib import Path
import matplotlib.pyplot as plt
from rasterio import plot
import rasterio
import geopandas
import pandas as pd
import numpy as np
from rasterio.mask import mask
import matplotlib.colors as colors
import matplotlib.cm as cmx
import pyproj
from bokeh.plotting import figure, show
from bokeh.io import output_notebook

from bokeh.tile_providers import OSM, get_provider
from bokeh.palettes import  Category10_10
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    CategoricalColorMapper
    )





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


def Color_mapper(point_color, color_map = "viridis"):
    #Get unique value from PandasSeries and removing NaN
    point_color.dropna(inplace = True)
    uniq = list(set(point_color))

    # Set the color map to match the uniq
    z = range(1,len(uniq))
    color_map = plt.get_cmap(color_map)
    cNorm  = colors.Normalize(vmin=0, vmax=len(uniq))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=color_map)

    return uniq, scalarMap




def InteractiveGeoPlotting(geo_df, size=None, color = None, point_size = 2, hover_data=None):
    df_geo = geo_df.copy()

    coord_x, coord_y = df_geo.geometry.x, df_geo.geometry.y
    
    ### TO DO: GET EPSG FROM DATASET
    proj = pyproj.Transformer.from_crs(32632, 3857, always_xy=True)
    
    

    coord_x, coord_y = proj.transform(coord_x, coord_y)

    df_geo["x"], df_geo["y"] = coord_x, coord_y

    p_df = df_geo.drop('geometry', axis=1).copy()

    output_notebook()
 
    if color:
        my_legend_name = str(p_df[color].name)
        p_df = p_df.loc[p_df[color].index]
        uniq, _ = Color_mapper(p_df[color])
        color_mapping = CategoricalColorMapper(factors=uniq, palette= Category10_10)
    else:
        pass

    tile_provider = get_provider(OSM)
    datasource = ColumnDataSource(p_df)


    min_x, max_x = min(p_df["x"]), max(p_df["x"])
    min_y, max_y = min(p_df["y"]), max(p_df["y"])

    # range bounds supplied in web mercator coordinates
    p = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
            x_axis_type="mercator", y_axis_type="mercator")
    p.add_tile(tile_provider)


    if color:

        p.circle(
                'x',
                'y',
                source=datasource,
                color=dict(field=my_legend_name, transform=color_mapping),
                legend_group=my_legend_name,
                line_alpha=1,
                fill_alpha=1,
                size=size if size else point_size)



    else:    


        p.circle(
                'x',
                'y',
                source=datasource,
                color="black",
                line_alpha=1,
                fill_alpha=1,
                size=size if size else point_size)


    
    my_hover = HoverTool()
    
    if hover_data:
        my_hover.tooltips = [(f'{hover_data[n]}', f'@{hover_data[n]}') for n, i in enumerate(hover_data)]
        p.add_tools(my_hover)

    show(p)