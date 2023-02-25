import os
import numpy as np
from osgeo import gdal, gdalconst

# set the input file path and name
input_file = "/path/to/input/file.tif"

# open the input file
dataset = gdal.Open(input_file, gdalconst.GA_Update)

# get the raster band
band = dataset.GetRasterBand(1)

# get the nodata value
nodata = band.GetNoDataValue()

# read the raster data as a numpy array
data = band.ReadAsArray()

# define the kernel size
kernel_size = 3

# define the kernel weights
kernel_weights = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

# find the indices of the no data values
indices = np.where(data == nodata)

# loop through the indices and interpolate the values
for i, j in zip(indices[0], indices[1]):
    # get the sub-array around the pixel
    sub_array = data[i-kernel_size//2:i+kernel_size//2+1, j-kernel_size//2:j+kernel_size//2+1]

    # compute the weighted average using the kernel weights
    interpolated_value = np.sum(sub_array * kernel_weights) / np.sum(kernel_weights)

    # replace the no data value with the interpolated value
    data[i, j] = interpolated_value

# write the updated data back to the raster band
band.WriteArray(data)

# close the dataset
dataset = None
