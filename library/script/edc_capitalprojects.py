import pandas as pd
import geopandas as gpd
import os
from os.path import join, dirname
from sqlalchemy import create_engine 
from dotenv import load_dotenv

from . import gdf_to_zip_tempfile

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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
        gdf = gpd.read_file("CCP_Jan_2022/CCP_Jan22_EDC.shp")
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
        pre = self.previous()
        new.columns = [x.lower() for x in new.columns]
        pre.drop(labels="ogc_fid", axis=1, inplace=True)
        
        new.rename(columns={"geometry": "wkb_geometry"},inplace=True)
        final = pre.append(new)
        final = final.drop_duplicates()
        #local_path = gdf_to_zip_tempfile(final)
        return final
