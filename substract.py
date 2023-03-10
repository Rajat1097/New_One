import rasterio

# Load the two DEMs
with rasterio.open('dem1.tif') as dem1:
    data1 = dem1.read(1)
    transform1 = dem1.transform

with rasterio.open('dem2.tif') as dem2:
    data2 = dem2.read(1)
    transform2 = dem2.transform

# Determine the overlapping extent
left, bottom, right, top = max(dem1.bounds.left, dem2.bounds.left), max(dem1.bounds.bottom, dem2.bounds.bottom), min(dem1.bounds.right, dem2.bounds.right), min(dem1.bounds.top, dem2.bounds.top)

# Calculate the overlapping window for each DEM
window1 = dem1.window(left, bottom, right, top)
window2 = dem2.window(left, bottom, right, top)

# Extract the overlapping portions of each DEM
overlap1 = data1[window1[0]:window1[1], window1[2]:window1[3]]
overlap2 = data2[window2[0]:window2[1], window2[2]:window2[3]]

# Subtract one DEM from the other in the overlapping area
result = overlap1 - overlap2

# Save the result as a new file or array
with rasterio.open('result.tif', 'w', driver='GTiff', width=result.shape[1], height=result.shape[0], count=1, dtype=result.dtype, crs=dem1.crs, transform=dem1.window_transform(window1)) as result_file:
    result_file.write(result, 1)
