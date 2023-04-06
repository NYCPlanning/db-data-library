from diagrams import Diagram, Cluster
from diagrams.onprem import client
from diagrams.programming import flowchart
from diagrams.programming import language
from diagrams.generic.blank import Blank
from diagrams.generic.database import SQL
from diagrams.digitalocean import storage

from library import config

web = flowchart.OffPageConnectorRight
manual = client.User

source_names = [
    "dcp_commercialoverlay",
    "dcp_limitedheight",
    "dcp_specialpurpose",
    "dcp_specialpurposesubdistricts",
    "dcp_zoningmapamendments",
    "dof_dtm",
    "dcp_zoningdistricts",
    "dcp_zoningmapindex"
]

overrides = {}

path = lambda name: f"./library/templates/{name}.yml"

def library_archive(source_node):
    processing_node = language.Python("Processing!")
    source_node >> processing_node
    return processing_node

def do(source, source_node):
    do_node = SQL(source)
    source_node >> do_node
    return do_node

class source:
    def __init__(self, name):
        if source in overrides: return overrides[name]
        self.name = name
        template = config.Config(path(name)).parsed_rendered_template()
        self.dataset = template["dataset"]
        self.source_type = self.dataset["source"]
        self.destination = self.dataset["destination"]

    def source(self):
        self.last_node = manual(self.name)

    def processing(self):
        node = language.Python("Processing!")
        self.last_node >> node
        self.last_node = node

    def do(self):
        node = SQL(self.name)
        self.last_node >> node
        self.last_node = node

sources = [ source(s) for s in source_names ]

with Diagram("ztl"):
    for s in sources: s.source()

    with Cluster("Library Archive"):
        for s in sources: s.processing()

    with Cluster("Digital Ocean"):
        #do = storage.Volume('edm-recipes')
        for s in sources: s.do()
    