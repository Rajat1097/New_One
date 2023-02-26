import rasterio
from rasterio.fill import fillnodata

tif_file = r"D:\dem.tif"
with rasterio.open(tif_file) as src:
    profile = src.profile
    arr = src.read(1)
    arr_filled = fillnodata(arr, mask=src.read_masks(1), max_search_distance=10, smoothing_iterations=0)

newtif_file = r"D:\dem_filled.tif"   
with rasterio.open(newtif_file, 'w', **profile) as dest:
    dest.write_band(1, arr_filled)
