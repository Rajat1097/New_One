import rasterio

with rasterio.open('lvis_data.tif') as dataset:
    lvis_data = dataset.read()
import numpy as np

# Find the location of missing values
missing_values = np.isnan(lvis_data)

# Replace missing values with 0
lvis_data[missing_values] = 0

from scipy.interpolate import interp2d

# Create a function to perform 2D cubic interpolation
interpolator = interp2d(np.arange(lvis_data.shape[1]), np.arange(lvis_data.shape[0]), lvis_data, kind='cubic')

# Create a grid of points where we want to interpolate the missing values
xx, yy = np.meshgrid(np.arange(lvis_data.shape[1]), np.arange(lvis_data.shape[0]))

# Interpolate the missing values
lvis_data[missing_values] = interpolator(xx[missing_values], yy[missing_values])

# Save the filled-in data to a new tiff file
with rasterio.open('lvis_data_filled.tif', 'w', **dataset.meta) as dataset:
    dataset.write(lvis_data)
