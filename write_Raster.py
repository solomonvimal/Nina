#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 22:22:06 2017

@author: svimal
"""
import os
import glob
import gdal
import osr
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['xtick.labelsize'] = 10

os.chdir("/home2/svimal/Data/Canada/MERIT_DEM/dem_tif_n30w120/merge")
os.system("gdalwarp -of gtiff -te " + str(-107.375-0.025) + " " + str(52.625-0.025) + " " +  str(-107.375+0.025) + " " + str(52.625+0.025) + " nelson_clippedfel.tif output.tif")

files = glob.glob("Redberry*")

slope_file = files[0]
Contrib_file = files[1]

slope = gdal.Open(slope_file, gdal.GA_Update).ReadAsArray()
Contrib = gdal.Open(Contrib_file, gdal.GA_Update).ReadAsArray()

newRasterfn = "twi.tif"
rasterfn = slope_file


def remove_zeros(slope):
    new = []
    for line in slope:
        for element in line:
            if element == 0:
                new.append(0.001)
            else:
                new.append(element)
    new_slope = numpy.array(new)
    new_slope = new_slope.reshape(slope.shape)
    return new_slope

new_slope = remove_zeros(slope)
new_Contrib = remove_zeros(Contrib)

array = new_Contrib/new_slope

plt.hist(array)

numpy.max(array)
numpy.percentile(array.flatten(), 70)

def array2raster(rasterfn,newRasterfn,array):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.SetNoDataValue(-9999)
    outband.FlushCache()

array2raster(rasterfn,newRasterfn,array)


array[array > 100000] = 100000

twi = array
#plt.hist(array.flatten())

dem_file = files[2]
dem = gdal.Open(dem_file, gdal.GA_Update).ReadAsArray()
plt.hist(dem.flatten())
# Select dem location with TWI greater than (1-area fraction) percentile
dem_twi = dem.copy()
dem_twi[twi<numpy.percentile(twi.flatten(), 80)]=0

# Remove the zeros and flatten it
dem_highTWI = dem_twi.flatten()[dem_twi.flatten()>0]

plt.figure(dpi=150)
plt.hist(dem.flatten()-numpy.min(dem.flatten()), label="DEM of entire grid")
plt.hist(dem_highTWI-numpy.min(dem_highTWI), label="DEM of wetland area \n (1-area fraction percentile TWI)")
plt.title("DEM histogram")
plt.xlabel("Elevation (m)")
plt.ylabel("Frequency")
plt.legend()


plt.hist(twi[twi>numpy.percentile(twi.flatten(), 70)].flatten(), label="TWI"); plt.legend()