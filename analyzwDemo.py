import pandas as pd
from ml_analyze import ml_analyze
import csv

def getDroppingFeatureResult(flights):
    WD = flights.drop("previous_price", 1)
    GD = flights[flights['collect_date'] > 27]
    LD = flights[flights['collect_date'] <= 27]

    nameMapFrame = {1: "WD",
                    2: "GD",
                    3: "LD"}

    WD = WD.drop("destination", 1)
    WD = WD.drop("days", 1)

    GD = GD.drop("destination", 1)
    GD = GD.drop("days", 1)

    LD = LD.drop("destination", 1)
    L = LD.drop("days", 1)

    dataFrameList = [WD, GD, LD]
    index = 1

    for data in dataFrameList:
        res = []
        print(nameMapFrame[index])
        for column in data:
            if column == "price":
                continue
            print("\ndrop " + column)
            temp= data.drop(column, 1)
            k = [0, 0, 0, 0, 0]
            for i in range(10):
                new_list = ml_analyze.analyze(flights=temp)
                k = [sum(i) for i in zip(k, new_list)]
                print(k)
            k = [x / 10 for x in k]
            res.append(k)
        fileNanme = nameMapFrame[index] + "_Phase_two.csv"
        with open(fileNanme, "w+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(res)
        index += 1

def getWholeDataSetComparing(flights):
    flights = flights.drop("previous_price", 1)
    flights = flights.drop("destination", 1)
    flights = flights.drop("days", 1)
    flights = flights.drop("airline", 1)

    ml_analyze.analyze(flights)


def getPhaseOneResult(flights):
    flights = flights.drop("previous_price", 1)
    df1 = flights[flights['collect_date'] > 27]
    df2 = flights[flights['collect_date'] <= 27]

    featureSet1 = ["depart_place", "destination", "distance0"]
    featureSet2 = ["depart_date", "return_date", "days"]

    dataFrameList = [df2]
    nameMapFrame = {1: "WD",
                    2: "GD",
                    3: "LD"}

    index = 1

    for data in dataFrameList:
        res = list()
        print(nameMapFrame[index])
        for f1 in featureSet1:
            for f2 in featureSet2:
                temp = data.drop(f1, 1)
                temp = temp.drop(f2, 1)
                print("Drop " + f1 + ", " + f2)
                k = [0, 0, 0, 0, 0]
                for i in range(10):
                    new_list = ml_analyze.analyze(flights=temp)
                    k = [sum(i) for i in zip(k, new_list)]
                    print(k)
                k = [x / 10 for x in k]
                res.append(k)
        fileNanme = nameMapFrame[index] + "_Phase_one.csv"
        with open(fileNanme, "w+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(res)



def getRunningTime(flights):
    flights = flights.drop("previous_price", 1)
    df1 = flights[flights['collect_date'] > 27]
    df2 = flights[flights['collect_date'] <= 27]

    flights = flights.drop("destination", 1)
    flights = flights.drop("days", 1)
    flights = flights.drop("airline", 1)

    df1 = df1.drop("depart_place", 1)
    df1 = df1.drop("return_date", 1)
    df1 = df1.drop("month", 1)

    df2 = df2.drop("destination", 1)
    df2 = df2.drop("days", 1)
    df2 = df2.drop("stops", 1)

    ml_analyze.analyze(flights)
    ml_analyze.analyze(df1)
    ml_analyze.analyze(df2)


if __name__ == '__main__':
    flights = pd.read_csv("november_11_result.csv")
    flights = flights.loc[flights["airline"] == "Air Canada"]
    #flights = flights[flights['collect_date'] > 27]
    getDroppingFeatureResult(flights)


























    # print("whole data set " + str(len(flights)))
    # ml_analyze.analyze(flights=flights)
    #
    # for column in flights:
    #     if column == "price":
    #         continue
    #     print("\ndrop " + column)
    #     drop_flights = flights.drop(column, 1)
    #     ml_analyze.analyze(flights=drop_flights)
    #
    #
    #
    # flights = df2
    # print("\n>27 " + str(len(flights)))
    # ml_analyze.analyze(flights=flights)
    # for column in flights:
    #     if column == "price":
    #         continue
    #     print("\ndrop " + column)
    #     drop_flights = flights.drop(column, 1)
    #     ml_analyze.analyze(flights=drop_flights)



    # print("drop stops")

    #print("> 27 days")
    # drop_flights = df1.drop("stops", 1)
    # #ml_analyze.analyze(flights=drop_flights)
    # #print("<27 days")
    # drop_flights = df2.drop("stops", 1)
    # #ml_analyze.analyze(flights=drop_flights)
    # #print("> 2 days and < 27 days")
    # drop_flights = df3.drop("stops", 1)
    # #ml_analyze.analyze(flights=drop_flights)
    #
    # print("drop stops and return_date")
    # print("whole data set")
    # drop_flights = flights.drop("stops", 1).drop("return_date", 1)
    # ml_analyze.analyze(flights=drop_flights)
    #
    # print("<27 days")
    # drop_flights = df2.drop("stops", 1).drop("return_date", 1)
    # ml_analyze.analyze(flights=drop_flights)
    # print("> 2 days and < 27 days")
    # drop_flights = df3.drop("stops", 1).drop("return_date", 1)
    # ml_analyze.analyze(flights=drop_flights)
    #
    #
    # print("> 2 days and < 27 days")
    # drop_flights = df3.drop("stops", 1).drop("return_date", 1).drop("destination", 1)
    # ml_analyze.analyze(flights=drop_flights)
    #
    # print("drop stops and destination")
    # print("<27 days")
    # drop_flights = df2.drop("stops", 1).drop("destination", 1)
    # ml_analyze.analyze(flights=drop_flights)
    # print("> 2 days and < 27 days")
    # drop_flights = df3.drop("stops", 1).drop("destination", 1)
    # ml_analyze.analyze(flights=drop_flights)



    #
    # # ml_analyze.analyze(flights=dataframe1)