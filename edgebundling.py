
# Testing out edge bundling with the MPA connections
# See discussion notes below and why I paused working on this.

# env: edgebundling

# https://datashader.org/user_guide/Networks.html#edge-rendering-bundling
# https://stackoverflow.com/questions/61333273/how-to-use-edge-bundling-with-networkx-and-matplotlib-in-python\
# https://datashader.org/_modules/datashader/bundling.html

import os
import math
import numpy as np
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from datashader.layout import random_layout, circular_layout, forceatlas2_layout
from datashader.bundling import connect_edges, hammer_bundle
from itertools import chain
import skimage
from skimage.filters import gaussian, sobel_h, sobel_v
import matplotlib.pyplot as plt


root = r'C:\Users\cristianij\Documents\Projects\edgebundling'
nodes_csv = os.path.join(root, 'spatial/nodes.csv')
conns = os.path.join(root, 'spatial/edges_pld{}.csv')
plds = ['1', '3', '7', '10', '21', '30', '40', '60']

# read in nodes
nodes = pd.read_csv(nodes_csv)

# hammer_bundle on connections
for pld in plds:
    #pld='60'
    conn = conns.format(pld)
    conn = pd.read_csv(conn)
    df = hammer_bundle(nodes, conn, weight='weight', initial_bandwidth=0.05, decay=0.7) # play around with these values
    break

# Test visualizing with matplotlib
df.plot(x="x", y="y", figsize=(9,9))

# Test symbolizing by different bundle
hbnp = df.to_numpy()
splits = (np.isnan(hbnp[:,0])).nonzero()[0]
start = 0
segments = []
for stop in splits:
    seg = hbnp[start:stop, :]
    segments.append(seg)
    start = stop

fig, ax = plt.subplots(figsize=(7,7))
#for seg in segments[::50]: # be every 50th segment
for seg in segments:
    ax.plot(seg[:,0], seg[:,1])


# So it seems like edgebundling doesn't leave separate components. They HAVE to all be connected
# by definition, even if by only one small connection.
# Keep in mind, this is about symbolizing graph structure, it does't know things like land barriers.

# Therefore, for my purposes, I don't think this helps me. I think it would just add confusion,
# even if technically those stepping stone connections are there.
# It looks like this function is still under development though, so maybe it will be useful in the
# future.
