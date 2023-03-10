import rasterio

with rasterio.open('dem1.tif') as src1:
    meta1 = src1.meta
    dem1 = src1.read(1)

with rasterio.open('dem2.tif') as src2:
    meta2 = src2.meta
    dem2 = src2.read(1)

from rasterio.coords import disjoint_bounds

bounds = disjoint_bounds([src1, src2])

from rasterio.warp import calculate_default_transform, reproject

if meta1['crs'] != meta2['crs'] or meta1['transform'] != meta2['transform']:
    transform, width, height = calculate_default_transform(src1.crs, src2.crs, src1.width, src1.height, *bounds)
    meta1.update({
        'crs': src2.crs,
        'transform': transform,
        'width': width,
        'height': height
    })
dem1 = reproject(dem1, meta1, src_crs=src1.crs, dst_crs=src2.crs, src_transform=src1.transform, dst_transform=transform, src_nodata=src1.nodata, dst_nodata=src2.nodata)
from rasterio.windows import from_bounds

window = from_bounds(*bounds, transform=meta1['transform'], width=meta1['width'], height=meta1['height'])

result = dem2.copy()
result[window] -= dem1[window]


with rasterio.open('result.tif', 'w', **meta2) as dst:
    dst.write(result, 1)
