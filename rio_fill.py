import rasterio
from scipy.interpolate import griddata
import numpy as np

# Load DEM
with rasterio.open('dem.tif') as src:
    dem = src.read(1)
    profile = src.profile

# Identify gaps
nodata_value = profile['nodata']
nodata_mask = (dem == nodata_value)

# Interpolate missing data
x, y = np.meshgrid(np.arange(0, dem.shape[1]), np.arange(0, dem.shape[0]))
x_missing = x[nodata_mask]
y_missing = y[nodata_mask]
z = dem[np.logical_not(nodata_mask)]
z_missing = griddata((x.flatten(), y.flatten()), z.flatten(), (x_missing, y_missing), method='linear')

# Fill gaps
dem_filled = dem.copy()
dem_filled[nodata_mask] = z_missing

# Save filled DEM
with rasterio.open('dem_filled.tif', 'w', **profile) as dst:
    dst.write(dem_filled, 1)
