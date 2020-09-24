from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

import pandas as pd

import time
import datetime

browser = webdriver.Chrome(executable_path='/Users/wzb/Downloads/chromedriver')

df = pd.DataFrame()


def compile_data(depart_place, return_place, depart_date, return_date):
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list

    #departure times
    dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]

    #arrival times
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]

    #airline name
    airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]

    #prices
    prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text for value in prices]

    #durations
    durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]

    #stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]

    #layovers
    layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
    layovers_list = [value.text for value in layovers]
    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_price = 'price'

    for i in range(len(dep_times_list)):

        try:
            df.loc[i, 'collect_date'] = current_date
        except Exception as e:
            pass

        try:
            df.loc[i, 'depart_place'] = depart_place
        except Exception as e:
            pass

        try:
            df.loc[i, 'destination'] = return_place
        except Exception as e:
            pass

        try:
            df.loc[i, 'depart_date'] = depart_date
        except Exception as e:
            pass

        try:
            df.loc[i, 'return_date'] = return_date
        except Exception as e:
            pass

        try:
            df.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'layovers'] = layovers_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, str(current_price)] = str(price_list[i])[1:]
        except Exception as e:
            pass
    print('Excel Sheet Created!')


now = datetime.datetime.now()
current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
current_time = (str(now.hour) + ':' + str(now.minute))
current_price = 'price'

depart_dates = ['09/02/2019', '09/04/2019', '09/04/2019', '09/05/2019', '09/06/2019', '09/07/2019', '09/08/2019']
return_dates = ['09/16/2019', '09/17/2019', '09/18/2019', '09/19/2019', '09/20/2019', '09/21/2019', '09/22/2019']
depart_places = ['Halifax', 'New York', 'Toronto', 'Vancouver', 'Calgary']
return_places = ['Halifax', 'New York', 'Toronto', 'Vancouver',  'Calgary']
i = 0
#04/01/2019', '04/02/2019', '04/03/2019','04/04/2019', '04/05/2019',
for depart_date in depart_dates:
    for return_date in return_dates:
        for depart_place in depart_places:
            for return_place in return_places:
                if return_place == depart_place:
                    continue
                link = "https://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:{0},to:{1},departure:{2}" \
                      "TANYT&leg2=from:{1},to:{0},departure:{3}TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%" \
                      "3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www." \
                      "expedia.com".format(depart_place, return_place, depart_date, return_date)
                browser.get(link)
                time.sleep(10)
                try:
                    compile_data(depart_place, return_place, depart_date, return_date)
                except:
                    continue
                df.to_csv("/Users/wzb/Documents/flight/9-1-Flights.csv", mode='a', header=False)
                df = df.iloc[0:0]

depart_places = ['Toronto', 'Beijing', 'Sydney', 'London']
return_places = ['Toronto', 'Beijing', 'Sydney', 'London']

for depart_date in depart_dates:
    for return_date in return_dates:
        for depart_place in depart_places:
            for return_place in return_places:
                if return_place == depart_place:
                    continue
                link = "https://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:{0},to:{1},departure:{2}" \
                      "TANYT&leg2=from:{1},to:{0},departure:{3}TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%" \
                      "3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www." \
                      "expedia.com".format(depart_place, return_place, depart_date, return_date)
                browser.get(link)
                time.sleep(10)
                try:
                    compile_data(depart_place, return_place, depart_date, return_date)
                except:
                    continue
                df.to_csv("/Users/wzb/Documents/International_flight/9-1-Flights.csv", mode='a', header=False)
                df = df.iloc[0:0]

depart_places = ['Toronto', 'Vancouver']
return_places = ['Los+Angeles']

for depart_date in depart_dates:
    for return_date in return_dates:
        for depart_place in depart_places:
            for return_place in return_places:
                if return_place == depart_place:
                    continue
                link = "https://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:{0},to:{1},departure:{2}" \
                      "TANYT&leg2=from:{1},to:{0},departure:{3}TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%" \
                      "3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www." \
                      "expedia.com".format(depart_place, return_place, depart_date, return_date)
                browser.get(link)
                time.sleep(10)
                try:
                    compile_data(depart_place, return_place, depart_date, return_date)
                except:
                    continue
                df.to_csv("/Users/wzb/Documents/International_flight/9-1-Flights.csv", mode='a', header=False)
                df = df.iloc[0:0]

import subprocess
subprocess.call(['osascript', '-e',
'tell app "System Events" to sleep'])

subprocess.call(['osascript', '-e',
'tell app "System Events" to sleep'])
