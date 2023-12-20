import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

"""
to install geopandas it's recommended you create a new environment using anaconda, and run this script within that environment:

Start --> Anaconda Prompt

conda create -n gpd python=3.9
conda activate gpd
conda install --channel conda-forge geopandas
"""

def lonlat_to_xy(lon,lat): 
    """
    Returns a full length cartesian co-ordinates as a tuple (x,y) given GPS lon/lat as input parameters 

    Parameters
    ----------

    lon : float64
        GPS longitude 

    lat : float64
        GPS latitude

    Returns
    -------

    Tuple
        Returns full length cartesian co-ordinates as a tuple (x,y)

    """
    d = {'lon': [lon], 'lat': [lat]}                                        # create a single pandas dataframe with GPS lon lat
    df = pd.DataFrame(data=d)                                               # define dataframe with tata above
    points = df.apply(lambda row: Point(row.lon, row.lat), axis=1)          # create points from co-ordinates, needed for geopandas conversion
    trains_data = gpd.GeoDataFrame(df, geometry=points)                     # create geodataframe from these points
    trains_data.crs = 'epsg:4326'                                           # init CRS Coordinate Reference System - convert to default cartesian standard epsg:4326
    trains_data = trains_data.to_crs('EPSG:31370')                          # convert to localized Belgian cartesian standard EPSG:31370
    xy_set = trains_data.get_coordinates()                                  # extract converted coordinates to a x/y dataframe length 1
    x = xy_set[0:1][['x']].values.tolist()[0][0]                            # extract x coordinate as a float64
    y = xy_set[0:1][['y']].values.tolist()[0][0]                            # extract y coordinate as a float64
    return (x,y)                                                            # return full length cartesian co-ordinates as a tuple 

print(lonlat_to_xy(4.438329,50.40424))

# import random
# for x in range(0,1000):
#     print(lonlat_to_xy(random.uniform(1.5, 9.0),random.uniform(45.0, 55.0)))
