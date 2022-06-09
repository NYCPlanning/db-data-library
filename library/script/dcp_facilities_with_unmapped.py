import pandas as pd
from zipfile import ZipFile
import requests

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def version(self):
        return self.config["dataset"]["version"]

    def ingest(self) -> pd.DataFrame:
        url = f"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/facilities_{self.version}csv.zip"
        r = requests.get(url, stream=True)
        with open(f"dcp_facilities_with_unmapped{self.version}.zip", "wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        with ZipFile(f"dcp_facilities_with_unmapped{self.version}.zip", "r") as zip:
            zip.extract(f"FacDB_{self.version}.csv")
            df = pd.read_csv(f"FacDB_{self.version}.csv", encoding="ISO-8859-1")
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path
