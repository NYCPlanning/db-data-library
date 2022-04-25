import pandas as pd
import geopandas as gpd
import os
from sqlalchemy import create_engine 
from dotenv import load_dotenv

from . import gdf_to_zip_tempfile

load_dotenv()

RECIPE_ENGINE = os.environ.get("RECIPE_ENGINE")

class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def version(self):
        return self.config["dataset"]["version"]

    @property
    def previous_version(self) -> str:
        return self.config["dataset"]["info"]["previous_version"]

    def ingest(self) -> gpd.GeoDataFrame:
        gdf = gpd.read_file("library/tmp/CCP_Jan_2022/CCP_Jan22_EDC.shp")

        gdf = gdf.to_crs("EPSG:2263")
        #gdf.insert(0, "v", self.version)
        return gdf

    def previous(self) -> gpd.GeoDataFrame:

        """
        this should be a process using sqlalchmy to ingest the previous projects 
        from the 
        it should be environmental variable set to correct postgres engine with the previous project loaded
        """
        db_connection_url = RECIPE_ENGINE
        con = create_engine(db_connection_url)  
        sql = "SELECT * FROM edc_capitalprojects"

        return gpd.GeoDataFrame.from_postgis(sql, con, geom_col="wkb_geometry")

    def runner(self) -> gpd.GeoDataFrame:
        new = self.ingest()
        prev = self.previous()
        new.columns = [x.lower() for x in new.columns]
        prev.drop(labels="ogc_fid", axis=1, inplace=True)
        new.rename(columns={"geometry": "wkb_geometry"},inplace=True)
        final = prev.append(new)
        final = final.drop_duplicates()
        print(final.geometry)
        local_path = gdf_to_zip_tempfile(final) # need to rewrite this with csv but first solve crs issue
        return local_path
