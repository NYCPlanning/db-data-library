import yaml
from typing import Literal, List
from pydantic import BaseModel, ValidationError, validator

VALID_ACL_VALUES = ('public-read', 'private')
VALID_GEOMETRY_TYPES = ('POINT', 'LINE', 'POLYGON', 'MULTIPOLYGON', 'MULTILINESTRING', 'LINESTRING', 'NONE')
VALID_SOCRATA_FORMATS = ('csv', 'geojson')

# Create schema
class GeometryType(BaseModel):
    SRS: str
    type: Literal[VALID_GEOMETRY_TYPES]

class Url(BaseModel):
    path: str # Specify field name and data type
    subpath: str = "" # Set default value

class Socrata(BaseModel):
    uid: str
    format: Literal[VALID_SOCRATA_FORMATS] # Use Literal[tuple(dtype)] to define specific, valid values

class SourceSection(BaseModel):
    url: Url = None # Pass another schema as a data type
    socrata: Socrata = None
    script: str = None
    geometry: GeometryType
    options: List[str] = [] # Use List[dtype] for a list field value

    print()
    @validator('url', 'socrata')    
    def validate_source(cls, v, values, **kwargs):
        print(values)
        return v


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
    """name: str
    version: str
    acl: Literal[VALID_ACL_VALUES]
    source: SourceSection
    destination: DestinationSection
    info: InfoSection = None"""
    source: SourceSection

class Validator:
    """ 
    Validator takes as input the path of a configuration file 
    and will run the necessary checks to determine wether the structure
    and values of the files are valid according to the requirements of
    the library.
    """

    def __load_file(self, path):
        with open(path, 'r') as stream:
            y = yaml.load(stream, Loader=yaml.FullLoader)
            return y

    # Check that source name matches filename and destination
    def dataset_name_matches(self, name, file) -> bool:
        dataset = file['dataset']
        return (dataset['name'] == name) and (dataset['name'] == dataset['destination']['name'])

    # Check that source has either an url or socrata field. NOT BOTH
    def has_url_or_socrata(self, file):
        dataset = file['dataset']
        source_fields = list(dataset['source'].keys())
        return ('url' in source_fields) ^ ('socrata' in source_fields)

    def validate_file(self, path):

        # Check if path ends with a .yml file
        extension = path.split('/')[-1].split('.')[-1]
        assert extension in ['yml', 'yaml'], 'Invalid file type'

        f = self.__load_file(path)
        name = path.split('/')[-1].split('.')[0]

        # TODO: Validate tree structure
      
        assert self.dataset_name_matches(name, f), 'Dataset name must match file and destination name'
        assert self.acl_is_valid(f), 'Invalid value for acl. It must be either "public-read" or "private"'
        assert self.has_url_or_socrata(f), 'Source cannot have both url and socrata' 
                
        return True   

    def tree_is_valid(self, file) -> bool:
        if(file['dataset'] == None):
            return False

        try:
            input_ds = Dataset(source=file['dataset']['source'])
            

        except ValidationError as e:
            print(e.json())
            return False
        
        
        return True
        