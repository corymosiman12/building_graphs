import json
import os
import sys
sys.path.append(os.getcwd())
from utils.utils import *

# Define the example file to use for the analysis.
# Clone the brick-examples repo to the same directory level
# as this repo.
ex_dir = os.path.join(os.getcwd(), '../brick-examples/haystack')
ex_file = os.path.join(ex_dir, "ghausi.json")
to_write = os.path.join(ex_dir, "ghausi-improved.json")

# Import the json file as a dictionary.
# This contains all entities in the building
bldg = import_haystack_json(ex_file)
bldg_len_original = len(bldg)

# Find all equipment entities
equips, non_equips = find_equips(bldg)
equips_len_original = len(equips)

# Find all fcus based on the navName.
# The fact that the navName contains FCU was found through
# exploratory analysis
fcus, non_fcu_equips = find_str_in_navName(equips, 'fcu')
fcu_len_original = len(fcus)

# Add 'fcu' tag to fcus
fcus = add_marker(fcus, 'fcu')

# Add all updated fcus and non_fcu_equips back into the building
bldg2 = non_equips.copy()
bldg2 += non_fcu_equips
bldg2 += fcus

# Check that 'fcu' tag added successfully
fcu2 = find_tagset(bldg2, tags=['equip', 'fcu'])
# Check that original equip numbers match
equip2 = find_equips(bldg2)

bldg2_len = len(bldg2)
equip2_len = len(equip2[0])
fcu2_len = len(fcu2[0])

# Script will exit if following checks don't hold
if bldg2_len != bldg_len_original:
    print("Number of entities in building changed.  Exiting.")
    print("Number of entities before fcu affected: {}".format(bldg_len_original))
    print("Number of entities after fcu affected: {}".format(bldg2_len))
    exit(1)

if equip2_len != equips_len_original:
    print("Number of equips in building changed.  Exiting.")
    print("Number of equips before fcu affected: {}".format(equips_len_original))
    print("Number of equips after fcu affected: {}".format(equip2_len))
    exit(1)

if fcu2_len != fcu_len_original:
    print("Number of fcus in building changed.  Exiting.")
    print("Number of fcus before fcu affected: {}".format(fcu_len_original))
    print("Number of fcus after fcu affected: {}".format(fcu2_len))
    exit(1)

# Find overlapping point entities
sen_cmds, non_sens_cmds = find_tagset(bldg2, tags=['sensor', 'cmd'])
sen_cmds_len1 = len(sen_cmds)

# Remove 'sensor' tag
sen_cmds2 = remove_tag(sen_cmds, 'sensor')

# Replace updated entities
bldg3 = non_sens_cmds.copy()
bldg3 += sen_cmds2

sen_cmds, non_sens_cmds = find_tagset(bldg3, tags=['sensor', 'cmd'])
sen_cmds_len2 = len(sen_cmds)

# Check that removal worked
if sen_cmds_len2 == sen_cmds_len1 and not sen_cmds_len1 == 0:
    print("No sensor-cmds changed.  Exiting")
    print("Number of points with both 'sensor' and 'cmd' tags\tOriginal: {}\tNew: {}".format(sen_cmds_len1,
                                                                                             sen_cmds_len2))
    exit(1)

# Now that duplicate point 'types' have been removed, find all point entities
sensors, not_sensors = find_sensors(bldg3)
cmds, not_cmds = find_cmds(not_sensors)
sps, not_sps = find_sps(not_cmds)

# print("sensor-sp: {}".format(len(sen_sps)))
# print("cmd-sp: {}".format(len(cmd_sps)))
# print(sen_cmds)


sens_len1 = len(sensors)
cmd_len1 = len(cmds)
sps_len1 = len(sps)

# Add point marker to all sensors, cmds, sps
sensors = add_marker(sensors, 'point')
cmds = add_marker(cmds, 'point')
sps = add_marker(sps, 'point')

# Repopulate building with sensors
bldg4 = not_sps.copy() + sensors + cmds + sps
bldg4_len = len(bldg4)

# Check numbers
sensors2, _ = find_tagset(bldg4, tags=['point', 'sensor'])
cmd2, _ = find_tagset(bldg4, tags=['point', 'cmd'])
sps2, _ = find_tagset(bldg4, tags=['point', 'sp'])
sens_len2 = len(sensors2)
cmd_len2 = len(cmd2)
sps_len2 = len(sps2)

if sens_len2 != sens_len1:
    print("Number of sensors in building changed.  Exiting.")
    print("Number of sensors before points affected: {}".format(sens_len1))
    print("Number of sensors after points affected: {}".format(sens_len2))
    exit(1)

if cmd_len2 != cmd_len1:
    print("Number of cmds in building changed.  Exiting.")
    print("Number of cmds before points affected: {}".format(cmd_len1))
    print("Number of cmds after points affected: {}".format(cmd_len2))
    exit(1)

if sps_len2 != sps_len1:
    print("Number of sps in building changed.  Exiting.")
    print("Number of sps before points affected: {}".format(sps_len1))
    print("Number of sps after points affected: {}".format(sps_len2))
    exit(1)

print("sensor-cmd\t\tOriginal: {}\tNew: {}".format(sen_cmds_len1, sen_cmds_len2))
print("Sensors\t\t\tOriginal: {}\tNew: {}".format(sens_len1, sens_len2))
print("Cmds\t\t\tOriginal: {}\tNew: {}".format(cmd_len1, cmd_len2))
print("Sps\t\t\tOriginal: {}\tNew: {}".format(sens_len1, sens_len2))
print("Building Entities\tOriginal: {}\tNew: {}".format(bldg_len_original, bldg4_len))
print("Equip Entities\t\tOriginal: {}\tNew: {}".format(equips_len_original, equip2_len))
print("FCU Entities\t\tOriginal: {}\tNew: {}".format(fcu_len_original, fcu2_len))
print("")
print("Checks cleared - serializing new JSON to {}".format(to_write))

to_serialize = {"rows": bldg4}
with open(to_write, 'w') as f:
    json.dump(to_serialize, f)
