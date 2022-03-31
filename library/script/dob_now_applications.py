import pandas as pd

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        df = pd.read_csv("s3://edm-private/dob_now/DOB_Now_Job_Filing_Data_for_DCP_{{ version }}.csv", encoding="Windows-1252")
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df, encode_utf_8=True)
        return local_path


