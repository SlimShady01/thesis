from math import sin, cos, sqrt, atan2, radians
from geopy.geocoders import Nominatim
geolocator = Nominatim()

def get_distance(city1, city2):
    R = 6373.0

    if city1 == "Halifax":
        city1 = "Halifax, NS"
    if city2 == "Halifax":
        city2 = "Halifax, NS"
    location1 = geolocator.geocode(city1)
    location2 = geolocator.geocode(city2)

    lat1 = radians(location1.latitude)
    lon1 = radians(location1.longitude)
    lat2 = radians(location2.latitude)
    lon2 = radians(location2.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
import pandas as pd
from dateutil import parser
import datetime
import glob
import numpy as np

df = pd.read_csv("flights.csv")
#print(df)
new_df = df
dic = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}

dic2 = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}
new_df['collect_date'] = new_df['collect_date'].apply(str)
new_df["return_date"] = (df["collect_date"].apply(int) + df["days"].apply(int)).apply(str)
# for i in range(len(df)):
#     num = dic[df.at[i, 'depart_date']] - int(df.at[i, 'collect_date']) % 7
#     if num <= 0:
#         num = num + 7
#     new_df.at[i, "collect_date"] = dic2[num]
#     new_df.at[i, "depart_date"] = df.at[i, 'collect_date']
#     new_df.at[i, "return_date"] = str(int(df.at[i, 'collect_date']) + int(df.at[i, 'days']))
#     new_df.at[i, "depart_place"] = str(int(get_distance(df.at[i, "depart_place"], df.at[i, "return_place"])))

new_df = new_df.drop(['destination', 'stops'], axis=1)
dic3 = {
    'HalifaxNew York': 956,
    'HalifaxToronto': 1263,
    'HalifaxVancouver': 4430,
    'HalifaxCalgary': 3757,
    'New YorkHalifax': 956,
    'New YorkToronto': 550,
    'New YorkVancouver': 3905,
    'New YorkCalgary': 3259,
    'TorontoHalifax': 1263,
    'TorontoNew York': 550,
    'TorontoVancouver': 3359,
    'TorontoCalgary': 2709,
    'VancouverHalifax': 4430,
    'VancouverToronto': 3359,
    'VancouverNew York': 3905,
    'VancouverCalgary': 674,
    'CalgaryHalifax': 3757,
    'CalgaryToronto': 2709,
    'CalgaryNew York': 3259,
    'CalgaryVancouver': 674
}

for i in range(len(new_df)):
    new_df.at[i, "depart_place"] = dic3[df.at[i, "depart_place"]+df.at[i, "destination"]]
print(new_df)
