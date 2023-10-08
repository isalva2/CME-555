# geopandas imports
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import geometry
from tqdm import tqdm

# geopandas imports
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import geometry

# function to create fishnets
def build_fishnet(gdf, square_size: int=2000):
    '''
    This function will build a "rasterized" mesh of the subject project area.
    '''
    # get gdf crs
    crs = gdf.crs

    # get extent of shapefile
    minX, minY, maxX, maxY = gdf.total_bounds

    # create fishnet
    x, y = (minX, minY)
    geom_array = []

    # loop through extent of gdf
    while y <= maxY:
        while x <= maxX:
            geom = geometry.Polygon([(x,y), (x, y+square_size), (x+square_size, y+square_size), (x+square_size, y), (x, y)])
            geom_array.append(geom)
            x += square_size
        x = minX
        y += square_size
    
    # build as GeoDataFrame
    fishnet = gpd.GeoDataFrame(geometry=geom_array, crs=crs)

    # perform left join on fishnet to retain original unit size
    filtered_fishnet = gpd.sjoin(fishnet, gdf, how="left", predicate="intersects").dropna()

    # keep only fishnet geometry, data to be populated while cross referencing data.
    fishnet_geometry = filtered_fishnet[["geometry"]]

    return fishnet_geometry

if __name__ == "__main__":
    '''
    Let's fishnet the chicago shapefile and save to the interim folder
    '''
    # directory
    import os
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, "../data")
    
    # load Cook County shapefile
    file = "interim/shp/chicago/chicago_epsg3435.shp"
    
    # load gdf
    chicago_gdf = gpd.read_file(
        os.path.join(
            data_path, file
        )
    )
    
    # create fishnet from cook county
    chicago_fishnet = build_fishnet(chicago_gdf, 500)
    
    # save to interim data
    chicago_fishnet.to_file(
        os.path.join(
            data_path, "interim/shp/fishnet/chicago_fishnet_500.shp"
        )
    )