import gdal
import osr
import ogr

# Open the DEM file using gdal library
dem_path = 'path/to/dem.tif'
ds = gdal.Open(dem_path)

# Get the spatial reference system and extent of the DEM file
srs = osr.SpatialReference()
srs.ImportFromWkt(ds.GetProjection())
geo_transform = ds.GetGeoTransform()
xmin, xmax, ymin, ymax = geo_transform[0], geo_transform[0] + geo_transform[1] * ds.RasterXSize, geo_transform[3] + geo_transform[5] * ds.RasterYSize, geo_transform[3]

# Create a shapefile for the contours
output_shapefile = 'path/to/contours.shp'
driver = ogr.GetDriverByName("ESRI Shapefile")
if os.path.exists(output_shapefile):
    driver.DeleteDataSource(output_shapefile)
out_ds = driver.CreateDataSource(output_shapefile)
out_lyr = out_ds.CreateLayer('contours', srs=srs)

# Set the contour interval and generate the contours
contour_interval = 10  # in meters
gdal.ContourGenerate(ds.GetRasterBand(1), contour_interval, 0, [], 0, 0, out_lyr)

# Close the shapefile and DEM file
out_ds = None
ds = None


import gdal
import osr
import ogr

# Open the DEM file using gdal library
dem_path = 'path/to/dem.tif'
ds = gdal.Open(dem_path)

# Get the spatial reference system and extent of the DEM file
srs = osr.SpatialReference()
srs.ImportFromWkt(ds.GetProjection())
geo_transform = ds.GetGeoTransform()
xmin, xmax, ymin, ymax = geo_transform[0], geo_transform[0] + geo_transform[1] * ds.RasterXSize, geo_transform[3] + geo_transform[5] * ds.RasterYSize, geo_transform[3]

# Create a shapefile for the contours
output_shapefile = 'path/to/contours.shp'
driver = ogr.GetDriverByName("ESRI Shapefile")
if os.path.exists(output_shapefile):
    driver.DeleteDataSource(output_shapefile)
out_ds = driver.CreateDataSource(output_shapefile)
out_lyr = out_ds.CreateLayer('contours', srs=srs)

# Set the contour interval and generate the contours
contour_interval = 10  # in meters
id_field = ogr.FieldDefn('elevation', ogr.OFTReal)
out_lyr.CreateField(id_field)
gdal.ContourGenerate(ds.GetRasterBand(1), contour_interval, 0, [], 0, 0, out_lyr, 0, 0)

# Close the shapefile and DEM file
out_ds = None
ds = None
