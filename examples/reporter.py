import os
import sys

sys.path.append(os.getcwd())
from utils.utils import *
from utils.plotting import *
import pandas as pd

"""
A simple script for building a report about a given Haystack project.

Modify the bldg_name to one of the files in the brick-examples/haystack directory.
Currently, one of:
    carytown
    gaithersburg
    ghausi
    ghausi-improved
    pes
    vrtdump
"""

bldg_name = "gaithersburg"
file_to_analyze = bldg_name + ".json"

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
reporter(report, bldg_name, bldg)

# # CSV filename
# csv_name = "report_{}.csv".format(bldg_name)
# output_dir = os.path.join(os.getcwd(), 'output', bldg_name)
# output_file = os.path.join(output_dir, csv_name)
#
# # Read in csv file as a dataframe
# df = pd.read_csv(output_file)
# plot1(df, output_dir, bldg_name)
