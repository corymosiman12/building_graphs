import numpy as np
import pandas as pd
import os
from plotnine import *

# Given a dataframe of the csv report produced by the reporter,
# Create a plot for each of the tag-categories, showing breakout of
# tags by entity types.
def plot1(df, output_dir, bldg_name):
    plot_dir = os.path.join(output_dir, 'plots')
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    types = np.unique(np.array(df['tag_category']))
    for t in types:
        df2 = df.loc[df['tag_category'] == t]
        p = ggplot(data=df2, mapping=aes(x='tag', y='count', fill='entity_type')) + \
            geom_bar(stat='identity') + \
            facet_grid('~entity_type', scales='free') + \
            labs(title="Building: " + bldg_name + "\nTag Type: " + t) + \
            coord_flip()
        f_name = os.path.join(plot_dir, bldg_name + "_" + t + '.png')
        ggplot.save(p, f_name, width=12, height=12, units='in', dpi=200)
            # geom_text(label='stat(count)') + \
