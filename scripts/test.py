from rdflib import RDF, RDFS, OWL, Namespace, Graph
import json
import os
from utils import *

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
ex_file = os.path.join(ex_dir, "ghausi-improved.json")

# Import the json file as a dictionary.
bldg = import_haystack_json(ex_file)

# Find all equipment entities
equips, not_equips = find_equips(bldg)

# Define tagset requirements for points
sensor_tags = ['point', 'sensor']
cmd_tags = ['point', 'cmd']
sp_tags = ['point', 'sp']

# Find all point entities
sensors, not_sensors = find_tagset(bldg, sensor_tags)
cmds, not_cmds = find_tagset(bldg, cmd_tags)
sps, not_sps = find_tagset(bldg, sp_tags)

# Define tags for equipment entities
# Quick check in the JSON file revealed these are the
# most common equip entities
vav_tags = ['equip', 'vav']
ahu_tags = ['equip', 'ahu']
fcu_tags = ['equip', 'fcu']
meter_tags = ['equip', 'meter']

vavs, equips2 = find_tagset(equips, vav_tags)
ahus, equips2 = find_tagset(equips2, ahu_tags)
fcus, equips2 = find_tagset(equips2, fcu_tags)
meters, equips2 = find_tagset(equips2, meter_tags)
exhaust_fans = find_str_in_navName(equips2, 'exhaust')

points, _ = find_tagset(bldg, ['point'])
# chosen = vavs[0]
# chosen_points = find_equip_points(chosen, sensors)

"""
Explore what all the other entities are.  For ghausi-improved.json, we have:
    Total Entities:     2183
    Total Sites:        0
    Total Floors:       0
    Total Zones:        0
    Total Spaces:       0
    Total Weather:      0
    Total Equips:       105
    Total Points:       1465
    Total VAVs:         20      These are exclusive vav types (not tagged as equips)
    Total HVACs:        1       Exclusive HVAC type (not tagged as equip)
"""
unique_keys = []
for e in bldg:
    for k in e.keys():
        unique_keys.append(k) if k not in unique_keys else None

unique_equip_keys = []
for e in equips:
    for k in e.keys():
        unique_equip_keys.append(k) if k not in unique_equip_keys else None

unique_point_keys = []
for p in points:
    for k in p.keys():
        unique_point_keys.append(k) if k not in unique_point_keys else None

ent_keys = set(unique_keys)
ent_keys = ent_keys.difference(set(unique_equip_keys))
ent_keys = ent_keys.difference(set(unique_point_keys))

ent_keys = list(ent_keys)
cnt = 0
for k in ent_keys:
    a, _ = find_tagset(bldg, [k])
    cnt += len(a)
    print("Tag: {}\t\t\tNumber: {}".format(k, len(a)))

print("Total number of Entities in the Building: {}".format(len(bldg)))
print("")
print("Total Number of Equips: {}".format(len(equips)))
print("Number of Equip-VAVs: {}".format(len(vavs)))
print("Number of Equip-AHUs: {}".format(len(ahus)))
print("Number of Equip-FCUS: {}".format(len(fcus)))
print("Number of Equip-Meters: {}".format(len(meters)))
print("Number of Exhaust Fans: {}".format(len(exhaust_fans)))
print("Number of Remaining Equips: {}".format(len(equips2)))
print("")
print("")
print("Total Number of Points: {}".format(len(points)))
print("Total Number of Point-Sensors: {}".format(len(sensors)))
print("Total Number of Point-Cmds: {}".format(len(cmds)))
print("Total Number of Point-Sps: {}".format(len(sps)))

print(ent_keys)
