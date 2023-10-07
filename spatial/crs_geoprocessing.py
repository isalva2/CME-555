import geopandas as gpd
import os

# link file to data/
current_dir = os.path.dirname(__file__)
data_path = data_path = os.path.join(current_dir, "../data")

# read chicago shp file (https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-City/ewy2-6yfk)
file =  "external/shp/Boundaries - City/geo_export_f3d57916-cb89-4faf-b26b-d00cef8241f9.shp"

# write to gdf and convert to EPSG: 3435 (https://spatialreference.org/ref/epsg/nad83-illinois-east-ftus/)
crs3435_chicago_gdf = gpd.read_file(
    os.path.join(data_path, file)
    ).to_crs(3435)

# write to interim data
crs3435_chicago_gdf.to_file(
    os.path.join(
        data_path, "interim/shp/chicago/chicago_epsg3435.shp")
    )

# read and write cook county shape file https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-City/ewy2-6yfk
file = "external/shp/Cook_County_Border/Cook_County_Border.shp"

# read file
cook = gpd.read_file(
    os.path.join(
        data_path, file
        )
    )

# write to interim
cook.to_crs(3435).to_file(
    os.path.join(
        data_path, "interim/shp/cook/cook_epsg3435.shp")
    )

# filter counties in CMAP region and export to interim https://hub-cookcountyil.opendata.arcgis.com/search?categories=boundaries%2Cgeometric%2Ctax%20district%2Ccounty%2Cstate%2Cfederal%2Cmunicipal%2Cunincorporated%20cook
file = "external/shp/IL_BNDY_County/IL_BNDY_County_Py.shp"

# list of counties in CMAP
CMAP_counties = ["COOK", "DUPAGE", "KANE", "KENDALL", "LAKE", "MCHENRY", "WILL"]

#read file
counties = gpd.read_file(
    os.path.join(
        data_path, file
        )
    )

# filter to CMAP counties and write to interim
counties[counties["COUNTY_NAM"].isin(CMAP_counties)].to_crs(3435).to_file(
    os.path.join(
        data_path, "interim/shp/cmap/cmap_epsg3435.shp"
        )
    )