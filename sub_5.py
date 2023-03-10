import rasterio
from rasterio.mask import mask
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
    # Convert the intersection to a GeoJSON-like geometry
    geometry = rasterio.features.geometry_mask(
        [intersection],
        out_shape=dem1.shape,
        transform=meta1['transform']
    )

    # Extract the overlapping area from the two rasters
    overlap1, overlap_transform = mask(src1, geometry, crop=True)
    overlap2, _ = mask(src2, geometry, crop=True)

    # Perform the subtraction of the overlapping area
    result = overlap2.copy()
    result -= overlap1

    # Write the result to a new raster file
    meta2.update({
        'transform': overlap_transform,
        'height': overlap1.shape[1],
        'width': overlap1.shape[2]
    })
    with rasterio.open('result.tif', 'w', **meta2) as dst:
        dst.write(result)

else:
    raise ValueError('The input rasters do not overlap.')
