import tempfile

import pandas as pd


def df_to_tempfile(df: pd.DataFrame) -> str:
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(f, index=False)
    return f.name

def gdf_to_zip_tempfile(gdf: pd.DataFrame) -> str:
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".shp")
    gdf.to_file(f, index=False)
    return f.name