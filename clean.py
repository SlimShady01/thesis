import pandas as pd
from dateutil import parser
import datetime
import glob

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

def clean(file_name, i):
    print(file_name + "is processing")
    df = pd.read_csv(file_name,
                    names=["index", "collect_date", "depart_place", "destination", "depart_date", "return_date",
                        "departure_time", "arrival_time", "airline", "duration", "stops", "layovers", "price"])

    df.drop('index', axis=1, inplace=True)
    df = df.dropna(how='any', axis=0)

    df = df.drop(df[df.stops == "(2 stops)"].index)
    df.loc[df['stops'] == '(Nonstop)', 'stops'] = 0
    df.loc[df['stops'] == '(1 stop)', 'stops'] = 1
    df = df.drop(df[df.stops == "(3 stops)"].index)
    df = df.drop(df[df.stops == "(4 stops)"].index)
    df = df.drop(df[df.stops == "(5 stops)"].index)
    df = df.drop(df[df.stops == "(6 stops)"].index)
    df = df.drop(df[df.stops == "(7 stops)"].index)
    f = df.dropna(how='any', axis=0)
    try:
        df = df.astype({"stops": int, "layovers": str})
    except:
        return

    df.loc[df['stops'] == 0, 'layovers'] = "0"
    df = df.dropna(how='any', axis=0)
    df.layovers = df.layovers.str[:1]

    df = df.reset_index(drop=True)
    now = datetime.datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)

    dic = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    }

    for i in range(len(df)):

        duration = int((parser.parse(df.iloc[i][8]) -
            parser.parse(str(parser.parse(df.iloc[i][8]))[0:10])).total_seconds() / 1800) * 30
        leaving_time = int((parser.parse(df.iloc[i][5]) - now).total_seconds()/10800)
        arriving_time = int((parser.parse(df.iloc[i][6]) - now).total_seconds()/10800)
        days = str((parser.parse(df.iloc[i][3]) - parser.parse(df.iloc[i][0])).days)
        #print(days)
        # if days[2] == 'd':
        #     days = days[0:1]
        # elif days == "0:00:00":
        #     days = "0"
        # else:
        #     days = days[0:2]

        days_diff = str(parser.parse(df.iloc[i][4]) - parser.parse(df.iloc[i][3]))[0:2]
        df.at[i, 'days'] = days_diff
        depart_day = dic[int(str(parser.parse(df.iloc[i][3]).weekday()))]
        return_day = dic[int(str(parser.parse(df.iloc[i][4]).weekday()))]

        df.at[i, 'depart_date'] = depart_day
        df.at[i, 'return_date'] = return_day
        df.at[i, 'departure_time'] = leaving_time
        df.at[i, 'arrival_time'] = arriving_time
        df.at[i, 'duration'] = duration
        df.at[i, 'collect_date'] = int(days)

        df.at[i, 'price'] = int(str(df.iloc[i][11]).replace(",", ""))

        df.at[i, "distance"] = int(dic3[df.at[i, "depart_place"] + df.at[i, "destination"]])

    #if i == 0:
    df = df[df['layovers'].apply(lambda x: str(x).isdigit())]
    df.to_csv('aprilFlights.csv', mode='a', header=False)
    # else:
    #     df.to_csv('flights.csv', mode='a', header=False)
    print(file_name + " is ready")

if __name__ == '__main__':
    path = "/Users/wzb/Documents/april-flight/*.csv"
    i = 0
    for file in glob.glob(path):
        clean(file, i)
        i += 1

