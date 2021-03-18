from functools import cached_property
from typing import List, Literal

import yaml
from pydantic import BaseModel, ValidationError, validator

VALID_ACL_VALUES = ("public-read", "private")
VALID_GEOMETRY_TYPES = (
    "POINT",
    "LINE",
    "POLYGON",
    "MULTIPOLYGON",
    "MULTILINESTRING",
    "LINESTRING",
    "NONE",
)
VALID_SOCRATA_FORMATS = ("csv", "geojson")

# Create schema
class GeometryType(BaseModel):
    SRS: str
    type: Literal[VALID_GEOMETRY_TYPES]


class Url(BaseModel):
    path: str  # Specify field name and data type
    subpath: str = ""  # Set default value


class Socrata(BaseModel):
    uid: str
    format: Literal[
        VALID_SOCRATA_FORMATS
    ]  # Use Literal[tuple(dtype)] to define specific, valid values


class SourceSection(BaseModel):
    url: Url = None  # Pass another schema as a data type
    socrata: Socrata = None
    script: str = None
    geometry: GeometryType
    options: List[str] = []  # Use List[dtype] for a list field value


class DestinationSection(BaseModel):
    name: str
    geometry: GeometryType
    options: List[str] = []
    fields: List[str] = []
    sql: str = None


class InfoSection(BaseModel):
    info: str = None
    url: str = None
    dependents: List[str] = None


class Dataset(BaseModel):
    name: str
    version: str
    acl: Literal[VALID_ACL_VALUES]
    source: SourceSection
    destination: DestinationSection
    info: InfoSection = None


class Validator:
    """
    Validator takes as input the path of a configuration file
    and will run the necessary checks to determine wether the structure
    and values of the files are valid according to the requirements of
    the library.
    """

    def __init__(self, path):

        # Abort if file path is not valid
        if not self.__check_extension(path):
            raise Exception("File path must point to a .yml or .yaml file")

        self.path = path
        self.fname = path.split("/")[-1].split(".")[0]

    def __check_extension(self, path):
        # Check if path ends with a .yml file
        extension = path.split("/")[-1].split(".")[-1]
        return extension in ["yml", "yaml"]

    @cached_property
    def file(self):
        with open(self.path, "r") as stream:
            y = yaml.load(stream, Loader=yaml.FullLoader)
            return y

    @property
    def tree_is_valid(self) -> bool:
        if self.file["dataset"] == None:
            return False

        try:
            input_ds = Dataset(**self.file["dataset"])

        except ValidationError as e:
            print(e.json())
            return False

        return True

    # Check that source name matches filename and destination
    @property
    def dataset_name_matches(self) -> bool:
        dataset = self.file["dataset"]
        return (dataset["name"] == self.fname) and (
            dataset["name"] == dataset["destination"]["name"]
        )

    # Check that source has only one source from either url, socrata or script
    @property
    def has_only_one_source(self):
        dataset = self.file["dataset"]
        source_fields = list(dataset["source"].keys())
        # In other words: if url is in source, socrata or script cannot be.
        # If url is NOT in source. Only one from socrata or url can be. (XOR operator ^)
        return (
            (("socrata" not in source_fields) and ("script" not in source_fields))
            if ("url" in source_fields)
            else (("socrata" in source_fields) ^ ("script" in source_fields))
        )

    @property
    def file_is_valid(self):

        name = self.path.split("/")[-1].split(".")[0]

        assert self.tree_is_valid, "Wrong fields"
        assert (
            self.dataset_name_matches
        ), "Dataset name must match file and destination name"
        assert (
            self.has_only_one_source
        ), "Source can only have one property from either url, socrata or script"

        return True
