from diagrams import Diagram
from diagrams.onprem import client
from diagrams.programming import flowchart
from diagrams.programming import language
from diagrams.generic.blank import Blank
from diagrams.digitalocean import storage

web = flowchart
manual = client.User

with Diagram("ztl"):
    dcp_commercialoverlay = manual("dcp_commercialoverlay")
    dcp_limitedheight = flowchart.Document("dcp_limitedheight")
    dcp_specialpurpose = flowchart.Document("dcp_specialpurpose")
    dcp_specialpurposesubdistricts = flowchart.Document("dcp_specialpurposesubdistricts")
    dcp_zoningmapamendments = flowchart.Document("dcp_zoningmapamendments")
    dof_dtm = flowchart.Document("dof_dtm")
    dcp_zoningdistricts = flowchart.Document("dcp_zoningdistricts")
    dcp_zoningmapindex = flowchart.Document("dcp_zoningmapindex")

    do = storage.Volume('edm-recipes')

    nodes = [ 
        dcp_commercialoverlay,
        dcp_limitedheight,
        dcp_specialpurpose,
        dcp_specialpurposesubdistricts,
        dcp_zoningmapamendments,
        dof_dtm,
        dcp_zoningdistricts,
        dcp_zoningmapindex,
    ]
    for node in nodes : 
        node >> do
