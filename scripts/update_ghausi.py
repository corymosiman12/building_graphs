import os
from utils.utils import *

# Define the example file to use for the analysis.
# Clone the brick-examples repo to the same directory level
# as this repo.
ex_dir = os.path.join(os.getcwd(), '../brick-examples/haystack')
ex_file = os.path.join(ex_dir, "ghausi.json")
to_write = os.path.join(ex_dir, "ghausi-improved.json")

# Import the json file as a dictionary.
bldg = import_haystack_json(ex_file)

# Find all equipment entities
equips = find_equips(bldg)

# Find all fcus based on the navName.
# The fact that the navName contains FCU was found through
# exploratory analysis
fcus, non_fcu_equips = find_str_in_navName(equips, 'fcu')

# Find all point entities
sensors, not_sensors = find_sensors(bldg)
cmds, not_cmds = find_cmds(not_sensors)
sps, not_sps = find_sps(not_cmds)

def add_marker(entities, marker_str):
    for e in entities:
        e[marker_str] = "M"
    return entities

# TODO: Add point marker to all sensors and all FCUs
sens = add_marker(sensors, 'point')
cmds = add_marker(cmds, 'point')
print(sens[0].keys())
