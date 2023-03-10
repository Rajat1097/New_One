import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS

# Load the two DEMs
with rasterio.open('dem1.tif') as src1, rasterio.open('dem2.tif') as src2:
    dem1 = src1.read(1)
    dem2 = src2.read(1)
    transform = src1.transform

# Check that the DEMs have the same spatial resolution and extent
if src1.bounds != src2.bounds or src1.width != src2.width or src1.height != src2.height or src1.crs != src2.crs:
    raise ValueError('DEMs do not have the same spatial resolution and extent')

# Subtract the elevation values of one DEM from the other
diff = dem2 - dem1

# Define a mask that includes only the ice field or glacier of interest
threshold = 3000 # change this to the elevation threshold that defines the ice field or glacier
mask = np.where(dem1 >= threshold, 1, 0)

# Multiply the difference DEM by the mask to isolate the changes on the ice field or glacier
diff_ice = diff * mask

# Calculate the volume change by multiplying the area of each pixel by the elevation change and summing over the ice field or glacier
pixel_area = abs(transform[0] * transform[4]) # area of each pixel in square meters
volume_change = np.sum(diff_ice) * pixel_area

# Write the volume change to a new GeoTIFF file
with rasterio.open('volume_change.tif', 'w', driver='GTiff', height=diff.shape[0], width=diff.shape[1], count=1, dtype=diff.dtype, crs=CRS.from_epsg(4326), transform=from_origin(src1.bounds.left, src1.bounds.top, transform[0], transform[4])) as dst:
    dst.write(diff_ice, 1)

print('Volume change:', volume_change, 'cubic meters')

