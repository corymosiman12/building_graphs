import os
from utils import *
from rdflib import RDFS, RDF, Namespace, Graph, URIRef

ex_dir = os.path.join(os.getcwd(), '../brick-examples/haystack')
ex_file = os.path.join(ex_dir, "pes.json")

# Load all entities in the building as a list of dicts
bldg = import_haystack_json(ex_file)

# Apply cleanup to marker tags for consistency
bldg = cleanup_marker_tags(bldg)

# Load all marker tags used in the building as a list of strings
bldg_markers = which_types(bldg)

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
