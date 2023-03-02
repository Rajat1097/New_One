import numpy as np
from osgeo import gdal
from scipy.interpolate import griddata

#Load the DEM file using the gdal library:
dem_path = 'path/to/dem.tif'
dem_dataset = gdal.Open(dem_path, gdal.GA_ReadOnly)


#Get the DEM data as a NumPy array:
dem_array = np.array(dem_dataset.GetRasterBand(1).ReadAsArray())

#identify the gaps in the DEM where values are NaN or NoData. 
#You can use the numpy.isnan() function to do this: python
is_nan = np.isnan(dem_array)
is_nodata = dem_array == dem_dataset.GetRasterBand(1).GetNoDataValue()
is_gap = np.logical_or(is_nan, is_nodata)

#Fill the gaps in the DEM using a nearest-neighbor interpolation:
# Get the indices of the gap pixels
gap_indices = np.transpose(np.nonzero(is_gap))

# Get the indices of the non-gap pixels
non_gap_indices = np.transpose(np.nonzero(np.logical_not(is_gap)))

# Get the pixel values of the non-gap pixels
non_gap_values = dem_array[non_gap_indices[:,0], non_gap_indices[:,1]]

# Interpolate the gap pixels using nearest-neighbor
interpolated_values = griddata(non_gap_indices, non_gap_values, gap_indices, method='nearest')

# Replace the gap pixels with the interpolated values
dem_array[is_gap] = interpolated_values

#Create a new TIFF file for the filled DEM
output_path = 'path/to/filled_dem.tif'
driver = gdal.GetDriverByName('GTiff')
output_dataset = driver.Create(output_path, dem_dataset.RasterXSize, dem_dataset.RasterYSize, 1, gdal.GDT_Float32)
output_dataset.SetGeoTransform(dem_dataset.GetGeoTransform())
output_dataset.SetProjection(dem_dataset.GetProjection())

#Write the filled DEM data to the new TIFF file:
output_dataset.GetRasterBand(1).WriteArray(dem_array)

dem_dataset = None
output_dataset = None







