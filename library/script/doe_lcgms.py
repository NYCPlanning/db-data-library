import json

import pandas as pd
import requests

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }
        body = "__EVENTTARGET=ctl00%24ContentPlaceHolder1%24LCGMSDataDownload%24Button1&__EVENTARGUMENT=&__VIEWSTATE=yIvVD8BwSY%2BlLHK0a2H5FrWQ9EfrSSDQJ8KOXQ35bVNi6lXZhoDmaN6E4NXNaP9uW8bnlP2kKxjdtLXh9vahuHowOFTad2L9Tn%2BtU8OtYlaUTy%2Fw&__VIEWSTATEGENERATOR=B9B96176&__EVENTVALIDATION=dVILHCjooNWW9mk0eGjjhFOG%2FUkgtEIoyjMwfnL7Uj3wvskyvfvrwtBduMszJp8aDcpQWtz%2B5MppvkLrbhcgapkIvidO1ncvM2Q6iDGB8hPJ7PF5"

        r = requests.post(
            "https://www.nycenet.edu/PublicApps/LCGMS.aspx", data=body, headers=headers
        )
        df = pd.read_html(r.text)
        df = df[0]  # first page of worksheet
        df.columns = df.iloc[0].str.replace("\t", " ")  # First row as column names
        df = df[1:]
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path
