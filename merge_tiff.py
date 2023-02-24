import os
from osgeo import gdal

# set the directory containing the TIFF files
directory = "/path/to/tiff/files"

# create a list of all TIFF files in the directory
tiff_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".tif")]

# set the output file name and path
output_file = "/path/to/output/file.tif"

# merge the TIFF files using gdal_merge.py function
gdal_command = "gdal_merge.py -o {} {}".format(output_file, " ".join(tiff_files))
os.system(gdal_command)
