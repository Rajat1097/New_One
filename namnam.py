import rasterio

with rasterio.open('dem1.tif') as src1, rasterio.open('dem2.tif') as src2:
    common_extent = src1.bounds.intersection(src2.bounds)
    
with rasterio.open('dem1.tif') as src1, rasterio.open('dem2.tif') as src2:
    window = rasterio.windows.from_bounds(*common_extent, transform=src1.transform)
    dem1 = src1.read(1, window=window)
    dem2 = src2.read(1, window=window)
    
 
 dem_diff = dem2 - dem1

    
profile = src1.profile.copy()
profile.update(count=1, dtype=rasterio.float32)
with rasterio.open('dem_diff.tif', 'w', **profile) as dst:
    dst.write(dem_diff.astype(rasterio.float32), 1)



