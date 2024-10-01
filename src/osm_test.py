import pandas as pd
import geopandas
import osmnx as ox

place_name = "Novosibirsk"

# Fetch OSM street network from the location
graph = ox.graph_from_place(place_name)
type(graph)
# Plot the streets
# fig, ax = ox.plot_graph(graph)

# List key-value pairs for tags
tags = {'building': True}

buildings = ox.features_from_place(place_name, tags)
buildings.head()
# Plot footprints
buildings.plot()
