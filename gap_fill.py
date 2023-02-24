import numpy as np
import os
import gdal
from scipy.interpolate import griddata

# set the input and output file paths
input_file = "/path/to/input/file.tif"
output_file = "/path/to/output/file.tif"

# open the input file
ds = gdal.Open(input_file)

# read the data from the input file
data = ds.ReadAsArray()

# find the locations of the gaps (where the data is NaN)
nan_mask = np.isnan(data)
y, x = np.indices(data.shape)

# create a mask for the valid data (where the data is not NaN)
valid_mask = ~nan_mask

# create arrays of the x, y, and data values for the valid data
x_valid = x[valid_mask]
y_valid = y[valid_mask]
data_valid = data[valid_mask]

# create arrays of the x and y values for the gaps
x_nan = x[nan_mask]
y_nan = y[nan_mask]

# interpolate the data for the gaps using griddata
data_interpolated = griddata((x_valid, y_valid), data_valid, (x_nan, y_nan), method='linear')

# fill the gaps with the interpolated data
data[nan_mask] = data_interpolated

# create the output file
driver = gdal.GetDriverByName("GTiff")
output = driver.Create(output_file, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32)
output.SetProjection(ds.GetProjection())
output.SetGeoTransform(ds.GetGeoTransform())

# write the data to the output file
output.GetRasterBand(1).WriteArray(data)

# close the input and output files
ds = None
output = None
