from rdflib import RDF, RDFS, OWL, Namespace, Graph
import json
import os
from utils.utils import *

# Instantiate a graph
g = Graph()

"""
We will choose an arbitrary URL for our namespace and refer to it by the
nickname "bldg" for convenience. "bldg" is also called a "prefix".
"""
BLDG1 = Namespace("http://my_buildings.com/bldg1")

g.bind("bldg1", BLDG1)

"""
Instantiate namespace requirements for Brick
"""
# BRICK contains brick classes and tagsets
BRICK = Namespace("https://brickschema.org/schema/1.0.3/Brick#")

# BF contains relationship definitions for brick
BF = Namespace('https://brickschema.org/schema/1.0.3/BrickFrame#')

"""
Instantiate namespace requirements for Project Haystack
"""
PH = Namespace("https://project-haystack.org/def/ph/3.9.7#")
PHICT = Namespace("https://project-haystack.org/def/phIct/3.9.7#")
PHSCIENCE = Namespace("https://project-haystack.org/def/phScience/3.9.7#")
PHIOT = Namespace("https://project-haystack.org/def/phIoT/3.9.7#")

# Define the example file to use for the analysis.
# Clone the brick-examples repo to the same directory level
# as this repo.
ex_dir = os.path.join(os.getcwd(), '../brick-examples/haystack')
ex_file = os.path.join(ex_dir, "ghausi.json")

# Import the json file as a dictionary.
bldg = import_haystack_json(ex_file)

# Find all equipment entities
equips = find_equips(bldg)

# Find all point entities
sensors, not_sensors = find_sensors(bldg)
cmds, not_cmds = find_cmds(not_sensors)
sps, not_sps = find_sps(not_cmds)

# Define tags for equipment entities
# Quick check in the JSON file revealed these are the
# most common equip entities
vav_tags = ['equip', 'vav']
ahu_tags = ['equip', 'ahu']
fcu_tags = ['equip', 'fcu']
meter_tags = ['equip', 'meter']

vavs, equips2 = find_tagset(equips, vav_tags)
ahus, equips2 = find_tagset(equips2, ahu_tags)
fcus, equips2 = find_str_in_navName(equips2, 'fcu')
meters, equips2 = find_tagset(equips2, meter_tags)
exhaust_fans, equips2 = find_str_in_navName(equips2, 'exhaust')

chosen = vavs[0]
chosen_points = find_equip_points(chosen, sensors)

print("Total number of Entities in the Building: {}".format(len(bldg)))

print("")
print("Total Number of Equips: {}".format(len(equips)))
print("Number of VAVs: {}".format(len(vavs)))
print("Number of AHUs: {}".format(len(ahus)))
print("Number of FCUS: {}".format(len(fcus)))
print("Number of Meters: {}".format(len(meters)))
print("Number of Exhaust Fans: {}".format(len(exhaust_fans)))
print("Number of remaining Equips: {}".format(len(equips2)))
print("")

num_points = len(sensors) + len(cmds) + len(sps)
print("Total Number of Points: {}".format(num_points))
print("Total Number of sensors: {}".format(len(sensors)))
print("Total Number of cmds: {}".format(len(cmds)))
print("Total Number of sps: {}".format(len(sps)))

