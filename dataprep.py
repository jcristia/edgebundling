
# Testing out edge bundling with the MPA connections


# https://datashader.org/user_guide/Networks.html#edge-rendering-bundling
# https://stackoverflow.com/questions/61333273/how-to-use-edge-bundling-with-networkx-and-matplotlib-in-python


import arcpy
import os
import pandas as pd

root = r'C:\Users\cristianij\Documents\Projects\edgebundling'
mpa_pts = os.path.join(root, 'spatial/COMBINED.gdb/patch_centroids')
exclude = os.path.join(root, 'spatial/mpas.gdb/M10_toexcludefromanalysis')
conns = os.path.join(root, 'spatial/COMBINED.gdb/conn_avg_pld{}')
plds = ['1', '3', '7', '10', '21', '30', '40', '60']


# add XY fields to patch centroids
fields = arcpy.ListFields(mpa_pts)
field_names = [field.name for field in fields]
if 'POINT_X' not in field_names:
    arcpy.AddXY_management(mpa_pts)

# read in as pandas df
cursor = arcpy.da.SearchCursor(mpa_pts, ['uID_202011', 'POINT_X', 'POINT_Y']) 
df = pd.DataFrame(data=[row for row in cursor], columns=['name', 'x', 'y'])

# exclude MPAs where oceaonographic models are not resolved
cursor = arcpy.da.SearchCursor(exclude, ['uID_20201124', 'exclude']) 
df_ex = pd.DataFrame(data=[row for row in cursor], columns=['name', 'exclude'])
df = df.merge(df_ex, on='name')
df = df[df.exclude.isna()]    # LOOK UP WHAT I DID IN THE PAST  . ALSO REMOVE EXCLUDE COLUMN
# list of uIDs to exclude
ex_list = list(df_ex.name[df_ex.exclude.isin([1,2])])

df.to_csv(os.path.join(root, 'spatial/nodes.csv'))



# connections to df to csv
for pld in plds:
    
    # read in as df
    conn = conns.format(pld)
    cursor = arcpy.da.SearchCursor(conn, ['from_id', 'to_id', 'prob_avg']) 
    df = pd.DataFrame(data=[row for row in cursor], columns=['source', 'target', 'weight'])

    # exclude certain mpas
    df = df[(~df.target.isin(ex_list)) & (~df.source.isin(ex_list))]

    # exclude self connections
    df = df[df.source != df.target]

    df.to_csv(os.path.join(root, f'spatial/edges_pld{pld}.csv'))
