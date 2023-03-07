# Fill Missing Rows with Data
# This script shows how to read an image where certain rows have missing data (i.e. 0) and fill that with the average of adjacent rows.
import rasterio
import numpy as np
filename = 'original.tif'
dataset = rasterio.open(filename)
metadata = dataset.meta
red = dataset.read(1)
green = dataset.read(2)
blue = dataset.read(3)
# The following returns an array where each item is True/False based on the condition `red==0`
result = np.all(red == 0, axis=1)
def average_rows(array, index):
    result = np.round(np.mean( np.array([array[index[0]-1], array[index[0]+1] ]), axis=0 ))
    array[index] = result
     
for index, x in np.ndenumerate(result):
    if (x and index[0] != 0 and index[0] != (dataset.height - 1)):
        average_rows(red, index)
        average_rows(blue, index)
        average_rows(green, index)
output_filename = 'fixed.tif'
metadata.update({'driver': 'GTiff'})
rgb_dataset = rasterio.open(output_filename, 'w', **metadata)
rgb_dataset.write(red, 1)
rgb_dataset.write(green, 2)
rgb_dataset.write(blue, 3)
rgb_dataset.close()
