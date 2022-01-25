import pandas as pd

import os
import sys

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def version(self):
        return self.config["dataset"]["version"]


    def encode_utf_8(self) -> pd.DataFrame:
        #df = pd.read_csv("dob_cofos.csv", dtype=str)

        df = pd.read_csv("dob_now_applications.csv", encoding='cp1252', encoding_errors='strict')

        df.to_csv('DOB_Now_Job_Filing_Data_for_DCP_20220125_encoded.csv', encoding='utf-8')

        #df.insert(0, "v", self.version)
        return df
