# Import necessary packages
import os
import geopandas as gpd
import rasterio as rio
import numpy as np

#Setting up directories
project =  "D:\\02_Portfolios\\00_Other\\03_NightLight\\"
raw = os.path.join(project, '01-data-raw')
process = os.path.join(project, '02-data-process', 'map_layers')
os.chdir(process)

raster_path = r"D:\02_Portfolios\00_Other\03_NightLight\01-data-raw\GEE\composite_2015_admin0_v2.tif"

#raster_path = r"D:\02_Portfolios\00_Other\03_NightLight\01-data-raw\diff_percent_2015_2020_v4.tif"


# Open raster
raster = rio.open(raster_path)
print(raster.read(1))

# Change nodata value
new_raster = np.nan_to_num(raster.read(1), nan =-9999)
print(new_raster)

# Register GDAL format drivers and configuration options with a
# context manager.
with rio.Env():
    profile = raster.profile
    with rio.open('composite_2015_admin0_v3.tif', 'w', **profile) as dst:
        dst.write(new_raster, 1)
