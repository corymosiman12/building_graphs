import os
import sys
sys.path.append(os.getcwd())
from utils.utils import *
from utils.queries import *

# Modify the following to one of the files in the brick-examples/haystack directory
file_to_analyze = "pes.json"

# Define location of brick-example/haystack
ex_dir = os.path.join(os.getcwd(), '../brick-examples/haystack')
ex_file = os.path.join(ex_dir, file_to_analyze)

if not os.path.isfile(ex_file):
    print("File does not exist: {}".format(ex_file))
    exit(1)

# Load all entities in the building as a list of dicts
bldg = import_haystack_json(ex_file)

# Apply cleanup to marker tags for consistency
bldg = cleanup_marker_tags(bldg)

# Load all marker tags used in the building as a list of strings
bldg_markers = only_markers(bldg)

# Using the Haystack 4 (3.9.7) defs.ttl, find the valid
# entities and markers
valid_hs_entities = ph_load_all_entities()
valid_hs_markers = ph_load_all_markers()
valid_hs_equips = ph_load_all_equips()
valid_hs_points = ph_load_pointFunctionTypes()

# Convert to sets for set operations
s_bldg_types = set(bldg_markers)
s_valid_hs_entities = set(valid_hs_entities)
s_valid_hs_markers = set(valid_hs_markers)


# Find all markers that are in either one or the other of the
# sets, but not both
m_sym_dif = s_valid_hs_markers.symmetric_difference(s_bldg_types)

# Find all types that are defined by the building, but
# are not valid Haystack types.  These are custom marker
# typings from the building
custom_bldg_types = s_bldg_types.difference(s_valid_hs_markers)
