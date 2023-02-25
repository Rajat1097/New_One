import gdal
import numpy as np
from pykrige.ok import OrdinaryKriging

# Read in the TIFF DEM file
src_ds = gdal.Open('dem.tif')
band = src_ds.GetRasterBand(1)

# Get the raster data and metadata
data = band.ReadAsArray()
no_data = band.GetNoDataValue()
geotransform = src_ds.GetGeoTransform()
projection = src_ds.GetProjection()

# Create a meshgrid of x and y coordinates
nx, ny = data.shape[1], data.shape[0]
x = np.linspace(geotransform[0], geotransform[0] + geotransform[1] * (nx - 1), nx)
y = np.linspace(geotransform[3], geotransform[3] + geotransform[5] * (ny - 1), ny)
xx, yy = np.meshgrid(x, y)

# Identify the missing values
mask = np.ma.masked_where(data == no_data, data)
missing = np.argwhere(mask.mask)

# Create the Kriging model
OK = OrdinaryKriging(x=missing[:, 1], y=missing[:, 0], z=mask.data[missing[:, 0], missing[:, 1]], variogram_model='linear')

# Fill the missing values using Kriging
z, ss = OK.execute(style='masked')

# Update the original data with the filled values
data[missing[:, 0], missing[:, 1]] = z.data

# Create a new TIFF file with the filled values
driver = gdal.GetDriverByName('GTiff')
dst_ds = driver.Create('dem_filled.tif', nx, ny, 1, gdal.GDT_Float32)
dst_ds.SetGeoTransform(geotransform)
dst_ds.SetProjection(projection)
dst_ds.GetRasterBand(1).WriteArray(data)
dst_ds.GetRasterBand(1).SetNoDataValue(no_data)
dst_ds.FlushCache()
