import os
import sys
sys.path.append(os.getcwd())
from utils.utils import *

"""
A simple script for building a report about a given Haystack project.
"""

# Modify the following to one of the files in the brick-examples/haystack directory
file_to_analyze = "ghausi-improved.json"

# Define location of brick-example/haystack
ex_dir = os.path.join(os.getcwd(), '../brick-examples/haystack/')
ex_file = os.path.join(ex_dir, file_to_analyze)

if not os.path.isfile(ex_file):
    print("File does not exist: {}".format(ex_file))
    exit(1)

# Load all entities in the building as a list of dicts
bldg = import_haystack_json(ex_file)

# Apply cleanup to marker tags for consistency
bldg = cleanup_marker_tags(bldg)

# Understand entities that have Haystack first class entities defined
report = ph_typer_many(bldg)
reporter(report, file_to_analyze)
