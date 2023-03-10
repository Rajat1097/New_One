import rasterio
from shapely.geometry import box

with rasterio.open('dem1.tif') as src1:
    meta1 = src1.meta
    bounds1 = src1.bounds
    dem1 = src1.read(1)

with rasterio.open('dem2.tif') as src2:
    meta2 = src2.meta
    bounds2 = src2.bounds
    dem2 = src2.read(1)

# Compute the intersection of the two bounding boxes
bbox1 = box(*bounds1)
bbox2 = box(*bounds2)
intersection = bbox1.intersection(bbox2)

# Check if the intersection is valid
if not intersection.is_empty:
    # Compute the window of the overlapping area
    bounds = intersection.bounds
    window = src1.window(*bounds)
else:
    raise ValueError('The input rasters do not overlap.')

# Perform the subtraction of the overlapping area
result = dem2.copy()
result[window] -= dem1[window]

# Write the result to a new raster file
with rasterio.open('result.tif', 'w', **meta2) as dst:
    dst.write(result, 1)
