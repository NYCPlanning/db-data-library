import importlib
import json
from datetime import datetime

import requests
import yaml
from jinja2 import Template

from .utils import format_url
from .validator import Validator


# Custom dumper created for list indentation
class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)


class Config:
    """
    Config will take a configuration file from the templates directly
    or any given configuration file and compute/output a configuration
    file to pass into the Ingestor
    """

    def __init__(self, path: str, version: str = None):
        # Validate file provided on path before initializing config class
        validator = Validator(path)

        if validator():
            self.path = path
            self.version = version
            # If validator passes all checks, use the parsed file
            self.file = validator.file
        else:
            raise Exception("Cannot create config object with the provided path")

    @property
    def source_type(self) -> str:
        """determine the type of the source, either url, socrata or script"""

        source = self.file["dataset"]["source"]

        if "url" in source.keys():
            return "url"
        if "socrata" in source.keys():
            return "socrata"
        return "script"

    def version_socrata(self, uid: str) -> str:
        """using the socrata API, collect the 'data last update' date"""
        metadata = requests.get(
            f"https://data.cityofnewyork.us/api/views/{uid}.json"
        ).json()
        version = datetime.fromtimestamp(metadata["rowsUpdatedAt"]).strftime("%Y%m%d")
        return version

    # @property
    # def version_bytes(self) -> str:
    #     """parsing bytes of the big apple to get the latest bytes version"""
    #     # scrape from bytes to get a version
    #     return None

    def valid_version(self, version: str) -> bool:
        """check that a version name is valid"""
        return "{" not in version and "}" not in version

    @property
    def version_today(self) -> str:
        """
        set today as the version name - for use with unspecified
        or invalid versions
        """
        return datetime.today().strftime("%Y%m%d")

    @property
    def compute(self) -> dict:
        """based on given yml file, compute the configuration"""
        if self.source_type == "script":
            if self.version:
                version = self.version
            else:
                version = self.version_today

            self.file["dataset"]["version"] = version

            script_name = self.file["dataset"]["source"]["script"]
            module = importlib.import_module(f"library.script.{script_name}")
            scriptor = module.Scriptor()
            url = scriptor.runner()

            options = self.file["dataset"]["source"]["options"]
            geometry = self.file["dataset"]["source"]["geometry"]
            self.file["dataset"]["source"] = {
                "url": {"path": url, "subpath": ""},
                "options": options,
                "geometry": geometry,
            }

        if self.source_type == "url":
            # Check for yml-specified
            # version (_version)
            _version = self.file["dataset"]["version"]

            # If a custom version specified from CLI, take custom version
            if self.version:
                version = self.version

            # If no custom version specified and version in config
            # is valid, take config version (_version)
            if not self.version and self.valid_version(_version):
                version = _version

            # If no custom version and no config version,
            # assign today as version
            if not self.version and not self.valid_version(_version):
                version = self.version_today

            # Assign version to .yml file
            self.file["dataset"]["version"] = version

        if self.source_type == "socrata":
            # For socrata we are computing the url and add the url object to the config file
            _uid = self.file["dataset"]["source"]["socrata"]["uid"]
            _format = self.file["dataset"]["source"]["socrata"]["format"]

            self.file["dataset"]["version"] = self.version_socrata(_uid)

            if _format == "csv":
                url = f"https://data.cityofnewyork.us/api/views/{_uid}/rows.csv"
            if _format == "geojson":
                url = f"https://nycopendata.socrata.com/api/geospatial/{_uid}?method=export&format=GeoJSON"

            options = self.file["dataset"]["source"]["options"]
            geometry = self.file["dataset"]["source"]["geometry"]
            self.file["dataset"]["source"] = {
                "url": {"path": url, "subpath": ""},
                "options": options,
                "geometry": geometry,
            }

        path = self.file["dataset"]["source"]["url"]["path"]
        subpath = self.file["dataset"]["source"]["url"]["subpath"]
        self.file["dataset"]["source"]["url"]["gdalpath"] = format_url(path, subpath)
        return self.file

    @property
    def compute_json(self) -> str:
        return json.dumps(self.compute, indent=4)

    @property
    def compute_yml(self) -> str:
        return yaml.dump(
            self.compute,
            Dumper=Dumper,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )

    @property
    def compute_parsed(self) -> (dict, dict, dict, dict):
        config = self.compute
        dataset = config["dataset"]
        source = dataset["source"]
        destination = dataset["destination"]
        info = dataset["info"]
        return dataset, source, destination, info
