import rasterio
from rasterio.coords import disjoint_bounds
from rasterio.windows import from_bounds

# Open the two DEMs
with rasterio.open('dem1.tif') as src1, rasterio.open('dem2.tif') as src2:
    
    # Read the metadata and data of the two DEMs
    meta1, meta2 = src1.meta, src2.meta
    dem1, dem2 = src1.read(1), src2.read(1)

    # Compute the common extent of the two DEMs
    bounds = disjoint_bounds([src1.bounds, src2.bounds])
    
    # Compute the overlapping window of the two DEMs
    window = from_bounds(*bounds, transform=meta1['transform'], width=meta1['width'], height=meta1['height'])
    
    # Subtract the two DEMs only where they overlap
    result = dem2.copy()
    result[window] -= dem1[window]
    
    # Update the metadata of the output raster
    meta2.update({
        'driver': 'GTiff',
        'height': result.shape[0],
        'width': result.shape[1],
        'transform': meta1['transform']
    })
    
    # Write the result to a new raster file
    with rasterio.open('result.tif', 'w', **meta2) as dst:
        dst.write(result, 1)
