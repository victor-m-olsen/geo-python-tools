# source code: https://towardsdatascience.com/zonal-statistics-algorithm-with-python-in-4-steps-382a3b66648a

import gdal
import ogr
import os
import numpy as np
import csv


def boundingBoxToOffsets(bbox, geot):
    col1 = int((bbox[0] - geot[0]) / geot[1])
    col2 = int((bbox[1] - geot[0]) / geot[1]) + 1
    row1 = int((bbox[3] - geot[3]) / geot[5])
    row2 = int((bbox[2] - geot[3]) / geot[5]) + 1
    return [row1, row2, col1, col2]


def geotFromOffsets(row_offset, col_offset, geot):
    new_geot = [
    geot[0] + (col_offset * geot[1]),
    geot[1],
    0.0,
    geot[3] + (row_offset * geot[5]),
    0.0,
    geot[5]
    ]
    return new_geot



def setFeatureStats(fid, mean, sum, dataset, names=["id", "mean", "sum", "dataset"]):
    featstats = {
    names[0]: fid,
    names[1]: mean,
    names[2]: sum,
    names[3]: dataset,
    }
    return featstats

mem_driver = ogr.GetDriverByName("Memory")
mem_driver_gdal = gdal.GetDriverByName("MEM")
shp_name = "temp"

fn_raster = "C:/Users/reach/Desktop/Private/Publication/8-propensity_score/Covariates-20210208T061559Z-001/Covariates/road_study_area.tif"
fn_zones = "C:/Users/reach/Desktop/Private/Publication/8-propensity_score/Conflict_variables-20210208T061556Z-001/Conflict_variables/5000m_sample/5000m_2017/conflict_sample_17_5k.shp"
dataset =  os.path.basename(fn_zones[:-4])

r_ds = gdal.Open(fn_raster)
p_ds = ogr.Open(fn_zones)

lyr = p_ds.GetLayer()
geot = r_ds.GetGeoTransform()
nodata = r_ds.GetRasterBand(1).GetNoDataValue()

zstats = []

p_feat = lyr.GetNextFeature()
niter = 0

while p_feat:
    if p_feat.GetGeometryRef() is not None:
        if os.path.exists(shp_name):
            mem_driver.DeleteDataSource(shp_name)
        tp_ds = mem_driver.CreateDataSource(shp_name)
        tp_lyr = tp_ds.CreateLayer('polygons', None, ogr.wkbPolygon)
        tp_lyr.CreateFeature(p_feat.Clone())
        offsets = boundingBoxToOffsets(p_feat.GetGeometryRef().GetEnvelope(),\
        geot)
        new_geot = geotFromOffsets(offsets[0], offsets[2], geot)

        tr_ds = mem_driver_gdal.Create(\
        "", \
        offsets[3] - offsets[2], \
        offsets[1] - offsets[0], \
        1, \
        gdal.GDT_Byte)

        tr_ds.SetGeoTransform(new_geot)
        gdal.RasterizeLayer(tr_ds, [1], tp_lyr, burn_values=[1])
        tr_array = tr_ds.ReadAsArray()

        r_array = r_ds.GetRasterBand(1).ReadAsArray(\
        offsets[2],\
        offsets[0],\
        offsets[3] - offsets[2],\
        offsets[1] - offsets[0])

        id = p_feat.GetFID()

        if r_array is not None:
            maskarray = np.ma.MaskedArray(\
            r_array,\
            maskarray=np.logical_or(r_array==nodata, np.logical_not(tr_array)))

            if maskarray is not None:
                zstats.append(setFeatureStats(\
                id,\
                maskarray.mean(),\
                maskarray.sum(), \
                dataset))

            else:
                zstats.append(setFeatureStats(\
                id,\
                nodata,\
                nodata,\
                nodata))
        else:
            zstats.append(setFeatureStats(\
                id,\
                nodata,\
                nodata,\
                nodata))

        tp_ds = None
        tp_lyr = None
        tr_ds = None

        p_feat = lyr.GetNextFeature()

fn_csv = "C:/Users/reach/Desktop/Private/Publication/8-propensity_score/zonal_stats/out1/zstats3.csv"
col_names = zstats[0].keys()

print(zstats)
with open(fn_csv, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, col_names)
    writer.writeheader()
    writer.writerows(zstats)
