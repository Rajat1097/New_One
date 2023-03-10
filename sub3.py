import rasterio

with rasterio.open('dem1.tif') as src1:
    meta1 = src1.meta
    bounds1 = src1.bounds
    dem1 = src1.read(1)

with rasterio.open('dem2.tif') as src2:
    meta2 = src2.meta
    bounds2 = src2.bounds
    dem2 = src2.read(1)

from rasterio.coords import disjoint_bounds

bounds = disjoint_bounds([bounds1, bounds2])

# Check if the bounds are valid
if bounds[0] < bounds[2] and bounds[1] < bounds[3]:
    # Compute the window of the overlapping area
    window = src1.window(*bounds)
else:
    raise ValueError('The input rasters do not overlap.')

# Perform the subtraction of the overlapping area
result = dem2.copy()
result[window] -= dem1[window]

# Write the result to a new raster file
with rasterio.open('result.tif', 'w', **meta2) as dst:
    dst.write(result, 1)
