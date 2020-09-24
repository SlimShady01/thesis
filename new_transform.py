import pandas as pd
import csv

df = pd.read_csv("aprilFlights.csv", names=["collect_date", "depart_place", "destination", "depart_date", "return_date",
                        "departure_time", "arrival_time", "airline", "duration", "stops", "layovers", "price", "days",
                                           "distance0"])

df = df.sort_values(by=['depart_place', 'destination', 'depart_date',
                        'return_date', 'departure_time', 'arrival_time', 'airline', 'duration',
                        'stops', 'days', 'distance0', 'collect_date'])
df = df.reset_index(drop=True)


for i in range(len(df)-1):
    if i == len(df):
        break
    # judge = (df.at[i, 'depart_place'] == df.at[i, 'depart_place']) and \
    #         (df.at[i, 'destination'] == df.at[i+1, 'destination']) and \
    #         (df.at[i, 'depart_date'] == df.at[i+1, 'depart_date']) and \
    #         (df.at[i, 'return_date'] == df.at[i + 1, 'return_date']) and \
    #         (df.at[i, 'departure_time'] == df.at[i + 1, 'departure_time']) and \
    #         (df.at[i, 'arrival_time'] == df.at[i + 1, 'arrival_time']) and \
    #         (df.at[i, 'airline'] == df.at[i + 1, 'airline']) and \
    #         (df.at[i, 'duration'] == df.at[i + 1, 'duration']) and \
    #         (df.at[i, 'stops'] == df.at[i + 1, 'stops']) and \
    #         (df.at[i, 'days'] == df.at[i + 1, 'days'])
    if int(df.at[i, "collect_date"]) - int(df.at[i+1, "collect_date"]) < 0:
        price = df.at[i+1, 'price']
        df.at[i, 'previous_price'] = price

df = df.dropna(how='any', axis=0)
df['month'] = "april"
print(len(df))


df1 = pd.read_csv("septemberFlights.csv", names=["collect_date", "depart_place", "destination", "depart_date", "return_date",
                        "departure_time", "arrival_time", "airline", "duration", "stops", "layovers", "price", "days",
                                           "distance0"])

df1 = df1.sort_values(by=['depart_place', 'destination', 'depart_date',
                        'return_date', 'departure_time', 'arrival_time', 'airline', 'duration',
                        'stops', 'days', 'distance0', 'collect_date'])
df1 = df1.reset_index(drop=True)


for i in range(len(df1)-1):
    if i == len(df1):
        break
    # judge = (df.at[i, 'depart_place'] == df.at[i, 'depart_place']) and \
    #         (df.at[i, 'destination'] == df.at[i+1, 'destination']) and \
    #         (df.at[i, 'depart_date'] == df.at[i+1, 'depart_date']) and \
    #         (df.at[i, 'return_date'] == df.at[i + 1, 'return_date']) and \
    #         (df.at[i, 'departure_time'] == df.at[i + 1, 'departure_time']) and \
    #         (df.at[i, 'arrival_time'] == df.at[i + 1, 'arrival_time']) and \
    #         (df.at[i, 'airline'] == df.at[i + 1, 'airline']) and \
    #         (df.at[i, 'duration'] == df.at[i + 1, 'duration']) and \
    #         (df.at[i, 'stops'] == df.at[i + 1, 'stops']) and \
    #         (df.at[i, 'days'] == df.at[i + 1, 'days'])
    if int(df1.at[i, "collect_date"]) - int(df1.at[i+1, "collect_date"]) < 0:
        price = df1.at[i+1, 'price']
        df1.at[i, 'previous_price'] = price

df1 = df1.dropna(how='any', axis=0)
df1['month'] = "september"
print(len(df1))

bigdata = df1.append(df, ignore_index=True)
bigdata.to_csv("november_11_result.csv", index=False)
print(len(bigdata))
