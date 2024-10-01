
import pandas as pd
import geopandas
from geodatasets import get_path
import osmnx as ox
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import time
import numpy as np


from context import pixel_to_ll, ll_to_pixel
from context import CustomFormatter
# vectorized haversine function
def haversine_distance(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371, to_meters=True):
    """
    Протестировано: https://www.omnicalculator.com/other/latitude-longitude-distance
    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2
    if to_meters == True:
        return 1000 * earth_radius * 2 * np.arcsin(np.sqrt(a))
    else:
        return earth_radius * 2 * np.arcsin(np.sqrt(a))

def createLocalMapDf(MAX_X, MAX_Y, MAX_LAT, MAX_LON, MIN_LAT, MIN_LON):

    lat_array = []
    lon_array = []
    x_array = []
    y_array = []
    for x in range(MAX_X):
        for y in range(MAX_Y):
            lat, lon = pixel_to_ll(x, y, MAX_Y, MAX_X, MAX_LAT, MAX_LON, MIN_LAT, MIN_LON)
            lat_array.append(lat)
            lon_array.append(lon)
            x_array.append(x)
            y_array.append(y)

    local = {
        "latitude":  lat_array,
        "longitude": lon_array,
        "x": x_array,
        "y": y_array
    }
    localDf = pd.DataFrame(local)
    return localDf

def calc_mean_attribute_val(attName, globalMapDataFrame, fromServerDataFrame):
    print(globalMapDataFrame.head().to_string())
    print(fromServerDataFrame.head().to_string())
    # df = fromServerDataFrame.reset_index()  # make sure indexes pair with number of rows

    for globalIndex, globalRow in globalMapDataFrame.iterrows():
        rsrp_by_distance_array = []
        for index, row in fromServerDataFrame[fromServerDataFrame.rsrp < 0].iterrows():
            # print(row.to_string())
            # print(globalRow.to_string())
            # print(row['geometry'], globalRow['geometry'])
            # print(row['geometry'].distance(globalRow['geometry']))
            d = haversine_distance(row['latitude'], row['longitude'],  globalRow['latitude'], globalRow['longitude'])
            if d <= 10:
                print(row['rsrp'])
                rsrp_by_distance_array.append(d)
        print("last d per globalRow: ", d)
        # if rsrp_by_distance_array != []:
        #     rsrp_distance_series = pd.Series(rsrp_by_distance_array)
        #     print(rsrp_distance_series.to_string())
        #     print("Mean = ", rsrp_distance_series.mean())
        #     time.sleep(10)
    return globalMapDataFrame
def main():
    # create logger with 'spam_application'
    logger = logging.getLogger("HeatMap")
    logger.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    logger.info("Starting Application")
    logger.info("Custom Logger is created")
    # change these to change how detailed the generated image is
    # (1000x1000 is good, but very slow)
    MAX_X=1000
    MAX_Y=1000

    # Границы планируемой местности
    MAX_LAT = 55.0388235
    MIN_LAT = 54.9693
    MAX_LON = 83.0272901
    MIN_LON = 82.8765452

    logger.info("Размер изображения: [%d, %d] (пикселей)", MAX_X, MAX_Y)
    logger.info("Границы карты:")
    logger.info("MAX[LAT, LON][%f, %f]", MAX_LAT, MAX_LON)
    logger.info("MIN[LAT, LON] [%f, %f]", MIN_LAT, MIN_LON)

    raw_df = pd.read_json('../data/thermalmapdataall.json')
    print(raw_df.head().to_string())
    gdf = geopandas.GeoDataFrame(
        raw_df, geometry=geopandas.points_from_xy(raw_df.latitude, raw_df.longitude), crs="EPSG:4326"
    )
    # print(gdf.head().to_string())

    world = geopandas.read_file(get_path("naturalearth.land"))
    # We restrict to South America.
    ax = world.clip([MIN_LON, MIN_LAT,MAX_LON, MAX_LAT]).plot(color="white", edgecolor="black")
    # We can now plot our ``GeoDataFrame``.
    # gdf.plot(ax=ax, color="red")
    # plt.show()

    pix_map_in_ll = createLocalMapDf(MAX_X, MAX_Y, MAX_LAT, MAX_LON, MIN_LAT, MIN_LON)
    gdf_pix_map_in_ll = geopandas.GeoDataFrame(
        pix_map_in_ll, geometry=geopandas.points_from_xy(pix_map_in_ll.latitude,pix_map_in_ll.longitude), crs="EPSG:4326"
    )
    # print(gdf_pix_map_in_ll.head().to_string())
    # gdf_pix_map_in_ll.plot(ax=ax, color="red", alpha=0.7)
    # plt.show()
    logger.info("Вычисляем значения каждого пикселя по атрибуту: ")
    time.sleep(1)
    calc_mean_attribute_val('rsrp', gdf_pix_map_in_ll, gdf)


if __name__ == "__main__":
    main()
