import os
import subprocess
from datetime import date
from urllib.parse import urlparse


def parse_engine(url: str) -> str:
    """
    url: postgres connection string
    e.g. postgresql://username:password@host:port/database
    """
    result = urlparse(url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    portnum = result.port
    return f"PG:host={hostname} port={portnum} user={username} dbname={database} password={password}"


def format_url(path: str, subpath: str) -> str:
    """
    Adds "vsis3" if [url] is from s3
    - s3://edm-recipes/recipes.csv

    Adds "vsizip" to [url] if [url] is zipped.
    - abcd.zip/abcd.shp
    - abcd.zip/abcd.csv
    - etc

    Adds "vsicurl" if [url] contains http
    - https://rawgithubcontent.come/somerepo/somefile.csv
    """
    if os.path.isfile(path):
        if ".zip" in path:
            return "/vsizip/" + path
        return path

    if len(subpath) > 0:
        subpath = subpath[1:] if subpath[0] == "/" else subpath
    path = path[:-1] if path[-1] == "/" else path
    url = path if len(subpath) == 0 else path + "/" + subpath

    if ".zip" in url:
        if "http" in url:
            url = "/vsizip/vsicurl/" + url
        elif "s3://" in url:
            url = "/vsizip/vsis3/" + url.replace("s3://", "")
        else:
            url = "/vsizip/" + url
        return url

    if "s3://" in url and ".zip" not in url:
        return url.replace("s3://", "/vsis3/")

    return url

def get_execution_details():
    timestamp = date.today().strftime("%Y-%m-%d %H:%M:%S")
    if os.environ.get("CI"):
        return {
            "type": "ci",
            "dispatch_event": os.environ['GITHUB_EVENT_NAME'],
            "url": f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
            "job": os.environ['GITHUB_JOB'],
            "timestamp": timestamp,
        }
    else:
        git_user = subprocess.run(["git", "config", "user.name"], stdout=subprocess.PIPE).stdout.strip().decode()
        return {
            "type": "manual",
            "user": git_user,
            "timestamp": timestamp,
        }
    