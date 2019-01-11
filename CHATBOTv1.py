# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:43:51 2018

@author: ging3
"""
from lxml import html
from datetime import time, date
from datetime import datetime
import re
import csv
import requests


class KnowledgeBase:
    kb_from_station_name = ""
    kb_to_station_name = ""
    kb_from_station_code = ""
    kb_to_station_code = ""
    kb_date = ""
    kb_time = ""
    kb_depart_or_arrive = ""
    kb_ret_date = ""
    kb_ret_time = ""
    kb_ret_depart_or_arrive = ""
    kb_command = ""
    kb_changes = ""

    def set_changes(self, changes):
        self.kb_changes = changes

    def set_from_station_code(self, from_station_code):
        self.kb_from_station_code = from_station_code

    def set_to_station_code(self, to_station_code):
        self.kb_to_station_code = to_station_code

    def set_command(self, command):
        self.kb_command = command

    def set_from_station(self, from_station):
        self.kb_from_station_name = from_station

    def set_to_station(self, to_station):
        self.kb_to_station_name = to_station

    def set_date(self, date):
        self.kb_date = date

    def set_time(self, time):
        self.kb_time = time

    def set_depart_or_arrive(self, depart_or_arrive):
        self.kb_depart_or_arrive = depart_or_arrive

    def set_return_date(self, ret_date):
        self.kb_ret_date = ret_date

    def set_return_time(self, ret_time):
        self.kb_ret_time = ret_time

    def set_return_depart_or_arrive(self, ret_depart_or_arrive):
        self.kb_ret_depart_or_arrive = ret_depart_or_arrive

    def remove_changes(self):
        self.kb_changes = ""

    def remove_command(self):
        self.kb_command = ""

    def remove_from_station(self):
        self.kb_from_station_name = ""

    def remove_to_station(self):
        self.kb_to_station_name = ""

    def remove_date(self):
        self.kb_date = ""

    def remove_time(self):
        self.kb_time = ""

    def remove_depart_or_arrive(self):
        self.kb_depart_or_arrive = ""

    def remove_return_date(self):
        self.kb_ret_date = ""

    def remove_return_time(self):
        self.kb_ret_time = ""

    def remove_return_depart_or_arrive(self):
        self.kb_ret_depart_or_arrive = ""

    def remove_from_station_code(self):
        self.kb_from_station_code = ""

    def remove_to_station_code(self):
        self.kb_to_station_code = ""

    def get_command(self):
        return self.kb_command

    def get_from_station(self):
        return self.kb_from_station_name

    def get_to_station(self):
        return self.kb_to_station_name

    def get_date(self):
        return self.kb_date

    def get_time(self):
        return self.kb_time

    def get_depart_or_arrive(self):
        return self.kb_depart_or_arrive

    def get_return_date(self):
        return self.kb_ret_date

    def get_return_time(self):
        return self.kb_ret_time

    def get_return_depart_or_arrive(self):
        return self.kb_ret_depart_or_arrive

    def get_from_station_code(self):
        return self.kb_from_station_code

    def get_to_station_code(self):
        return self.kb_to_station_code

    def get_changes(self):
        return self.kb_changes

    def clear_kb(self):
        kb_from_station_name = ""
        kb_to_station_name = ""
        kb_from_station_code = ""
        kb_to_station_code = ""
        kb_date = ""
        kb_time = ""
        kb_depart_or_arrive = ""
        kb_ret_date = ""
        kb_ret_time = ""
        kb_ret_depart_or_arrive = ""
        kb_command = ""


class GAChatBot:

    def __init__(self):
        # kb_from_station_code = ""
        # kb_to_station_code = ""

        # GETS TODAY DATE AND TIME AND SEPERATES THEM
        self.d = datetime.now().strftime("%d%m%y %H%M")
        date, space, time = self.d.partition(' ')
        kb.set_date(kb, date)
        kb.set_time(kb, time)
        # kb_date, space, kb_time = d.partition(' ')
        self.dflag = 0
        self.tflag = 0

        self.kb_return = False

        # ret_date, space2, ret_time = self.d.partition(' ')
        # kb.set_return_date(kb, ret_date)
        # kb.set_return_time(kb, ret_time)
        # kb_ret_date, space2, kb_ret_time = d.partition(' ')
        kb_command = ''

        self.cb_flag = 0
        self.cb_running = True

        # Key Words and Phrases
        self.train_station = []
        data = csv.reader(open("norfolk_stations.csv"))
        for line in data:
            # print(line)
            self.train_station.append(re.sub(r'[^a-zA-Z0-9 ]+', '', str(line).lower()))

        self.OPENING_PHRASES = ("Hello, I am TrainBot how could I help?")
        self.MONTHS = (
            "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
            "november",
            "decemeber")
        self.TIME_CONTAIN = ("am", "pm")

        # REGEX
        self.date_regex = ('\d{2}/\d{2}/\d{4}')
        self.time_regex = ('^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')

    def run_bot(self):
        while self.cb_running is True:

            print(kb.get_from_station(kb), kb.get_to_station(kb), kb.get_date(kb), kb.get_time(kb),
                  kb.get_return_date(kb))
            if kb.get_return_date(kb) != '':
                print(kb.get_return_date(kb), kb.get_return_time(kb))
            user_input = input("USER: ")
            # print(self.DATE)
            # self.DATE = self.DATE.replace(year = 2017, hour = 13)
            # print(self.DATE)
            if user_input == "stop":
                self.cb_running = False
            else:

                if self.cb_flag == 1:
                    print("")
                    if "yes" in user_input.lower():
                        # WHERE THE PROGRAM CALLS THE FIND TRAIN TICKET FUNCTION
                        # RENAME IF NEEDED - JACK
                        pm.trainData(pm)
                        self.findTrainTimes()
                        kb.clear_kb(kb)
                        self.cb_flag = 0
                        self.dflag = 0
                        self.tflag = 0
                    else:
                        kb.clear_kb(kb)
                        self.cb_flag = 0
                        self.dflag = 0
                        self.tflag = 0
                        print("okay, lets try that again, what is your journey?")
                else:
                    self.listen(user_input)
                    self.respond(user_input)

    def listen(self, sentence):
        words = sentence.split()
        if "return" in sentence.lower():
            self.kb_return = True
        for counter, word in enumerate(words):

            if word.lower() in self.train_station:
                if words[counter - 1] is "to" or kb.get_from_station(kb) is not "empty":
                    kb.set_to_station(kb, word.lower())
                else:
                    kb.set_from_station(kb, word.lower())
                    print(kb.get_from_station(kb))
                    # date capture - only 1 method implemented with format "dd/mm/yy"
            elif re.search(self.date_regex, word) and self.dflag == 0:
                self.dflag = 1
                self.kb_date = word
            elif re.search(self.time_regex, word) and self.tflag == 0:
                self.tflag = 1
                self.kb_time = word
            elif self.kb_return is True:
                if re.search(self.date_regex, word):
                    self.kb_ret_date = word
                elif re.search(self.time_regex, word):
                    self.kb_ret_time = word

    def respond(self, setence):
        start = "BOT: "
        answer = "You still need to enter your"
        if kb.get_from_station(kb) == "empty":
            answer = answer + " starting station "
        if kb.get_to_station(kb) == "empty":
            if answer == "You still need to enter your":
                answer = answer + " destination station "
            else:
                answer = answer + "and destination station"

        # checks if they still need minimum information
        if answer != "You still need to enter your":
            print(start + answer)
        else:
            response = "You are traveling from " + kb.get_from_station(kb) + " to " + kb.get_to_station(kb) + " on "
            response = response + kb.get_date(kb) + " at " + kb.get_time(kb)

            if kb.get_return_date(kb) != '':
                response = response + " and returning on the "
                if kb.get_return_date(kb) == kb.get_date(kb):
                    response = response + "same day at " + kb.get_return_time(kb)
                else:
                    response = response + kb.get_return_date(kb) + " at " + kb.get_return_time(kb)
            print(response + ". Is that Correct?")
            self.cb_flag += 1

    def findTrainTimes(self):
        expecting_date = False
        csv_file = csv.reader(open('norfolk_station_codes_with_names.csv', "rt"), delimiter=",")
        from_station = ''
        to_station = ''
        from_station_name = kb.get_from_station(kb)
        to_station_name = kb.get_to_station(kb)
        if (from_station_name is not '') and (to_station_name is not ''):
            for row in csv_file:
                if (from_station_name in row[0].lower()) or (from_station_name in row[1].lower()):
                    from_station_name = row[0]
                    from_station = row[1]
                elif (to_station_name in row[0].lower()) or (to_station_name in row[1].lower()):
                    to_station_name = row[0]
                    to_station = row[1]
            while expecting_date & (kb.get_date(kb) == ''):
                print("Please enter a date, entering no date will set date to today")
                expecting_date = False

            if (from_station != "") & (to_station != ""):
                url = "http://ojp.nationalrail.co.uk/service/timesandfares/" + from_station + "/" + to_station
                if kb.get_date(kb) == "":
                    kb.set_date(kb, 'today')
                url = url + "/" + kb.get_date(kb)
                if to_station == "":
                    kb_time = str(datetime.datetime.now().kb_time())
                    kb_time = kb_time[0:2] + kb_time[3:5]
                url = url + "/" + kb.get_time(kb)
                if kb.get_depart_or_arrive(kb) == "":
                    kb_depart_or_arrive = "dep"
                url = url + "/" + kb_depart_or_arrive
                if kb.get_return_date(kb) != "":
                    url = url + "/" + kb.get_return_date(kb)
                    if kb.get_return_time(kb) == "":
                        url = url + "/" + "0900/first"
                    else:
                        url = url + "/" + kb.get_return_time(kb)
                        if kb.get_return_depart_or_arrive(kb) == "":
                            url = url + "/dep"
                        else:
                            url = url + "/" + kb.get_return_depart_or_arrive(kb)
                    page = requests.get(url)
                    tree = html.fromstring(page.content)
                    price = tree.xpath('//*[@id="singleFaresPane"]/strong/text()')
                else:

                    page = requests.get(url)
                    tree = html.fromstring(page.content)
                    price = tree.xpath('//*[@id="fare-switcher"]/div/a/strong/text()')

                price = re.sub(',.*$|[^£\d\.]', '', str(price))
                num_changes = re.sub('[^\d]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[6]/text()')))
                kb.set_changes(num_changes)
                f_time_dep = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[1]/text()')))
                f_time_arr = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[4]/text()')))
                f_price = re.sub('[^£\d\.]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[9]/div/label/text()')))
                service = re.sub('[^A-Za-z ]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[8]/div/div/a/text()')))
                ret_dep_time = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="ift"]/tbody/tr[1]/td[1]/text()')))
                ret_arr_time = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="ift"]/tbody/tr[1]/td[4]/text()')))
                ret_f_price = re.sub('[^£\d\.:]', '',
                                     str(tree.xpath('//*[@id="ift"]/tbody/tr[1]/td[9]/div[2]/label/text()')))
                ret_date = kb.get_return_date(kb)
                date = kb.get_date(kb)

                if ret_date == "":
                    output = "The train closest to your chosen time leaves " + kb.get_from_station(kb) + " at " \
                             + f_time_dep + " on "
                    if date != 'today':
                        output = output + " " + date[:2] + "/" + date[2:4] + "/" + date[4:8]
                    else:
                        output = output + " on " + date
                    output = output + " costing " + f_price

                    if price == f_price:
                        output = output + ". This is the cheapest fare around those times." \
                                          " This service is currently running: " + service
                    else:
                        output = output + "\n" + "Cheapest price found from " + from_station_name + " to " + to_station_name \
                                 + " for " + price + ". This service is currently running: " + service

                else:
                    print(url)
                    ret_f_price = re.sub('[^\d]', '', ret_f_price)
                    f_price = re.sub('[^\d]', '', f_price)
                    total_price = float(f_price) + float(ret_f_price)
                    total_price = total_price / 100
                    total_price = str("£" + "%.2f" % total_price)
                    output = "The train closest to your chosen time leaves " + from_station_name + " at " \
                             + f_time_dep + " and arrives at " + to_station_name + " at " + f_time_arr
                    if date != 'today':
                        output = output + " " + date[:2] + "/" + date[2:4] + "/" + date[4:8]
                    else:
                        output = output + " on " + date
                    output = output + ".\nYour return journey will leave " + to_station_name + " at " + ret_dep_time \
                             + " and arrives at " + from_station_name + " at " + ret_arr_time
                    if ret_date != 'today':
                        output = output + " on " + ret_date[:2] + "/" + ret_date[2:4] + "/" + ret_date[4:8]
                    else:
                        output = output + ret_date
                    output = output + ".\nThis journey will cost " + total_price
                    if total_price != price:
                        output = output + "\nCheaper return journey from " + from_station_name + " to " + to_station_name \
                                 + " for " + price + " is available."

                        # TODO: ADD 'NEXT TRAIN'
                        # TODO: ADD 'FIRST/LAST TRAIN'
                        # TODO: COMMENTS
                print(output)
                print(url)

            print("")
        if to_station_name == '':
            print('To Station Error')

        if from_station_name == '':
            print('from station name error')


import numpy as np


class PredictionModel:

    def __init__(self):

        # generating the seed for the random number
        np.random.seed(1)

        # converting the weights, based on a 3 integer array representing information
        # about the train route, and a 1 integer array based on whether the train is 
        # late or not
        self.weights = 2 * np.random.random((3, 1)) - 1

        # applies the sigmoid function to normalise sum of the inputs

    def sigmoid(self, x):

        return 1 / (1 + np.exp(-x))

    # calculates the derivative to the sigmoid function above for weight adjustments
    def sigmoidDerivative(self, x):

        return x * (1 - x)

    # trains the prediction model to understand and learn the outcomes of the train
    # routes based on the information given by the 2 arrays mentioned above   
    def weightAdjustment(self, routeInformation, routeLate, trainingIterations):

        for iteration in range(trainingIterations):
            # iterates through each instance of a train route information
            output = self.prediction(routeInformation)

            # computes the back propogation outcome
            error = routeLate - output

            # adjusts weights using sigmoid derivative to enhance accuracy
            adjustments = np.dot(routeInformation.T, error * self.sigmoidDerivative(output))

            self.weights += adjustments

    # passes new data through the instances in the model to receive accurate
    # prediction based on the weights calculated earlier  
    def prediction(self, inputs):

        inputs = inputs.astype(float)
        output = self.sigmoid(np.dot(inputs, self.weights))
        return output

    def timeMean(self, times):

        mean = 0
        count = 0

        for number in times:
            mean = (mean + number)
            count += 1

        mean = mean / count

        mean = int(round(mean))

        return mean

    def trainData(self):

        trainPredictions = PredictionModel()
        # departing_station = kb.get_from_station(kb).lower()
        # arrival_station = kb.get_to_station(kb)
        departing_station = 'norwich'
        arrival_station = 'acle'
        trainRoute = departing_station + " to " + arrival_station

        print("Your route is ", trainRoute)
        temp_date = kb.get_date(kb)
        day = date(int('20' + temp_date[4:6]), int(temp_date[2:4]), int(temp_date[:2]))
        print(day)
        dayOfTravel = day.weekday()
        if dayOfTravel >= 6:
            day = 1
        else:
            day = 0

        url = "http://ojp.nationalrail.co.uk/service/timesandfares/ACL/NRW/tomorrow/1445/dep"
        page = requests.get(url)
        tree = html.fromstring(page.content)
        number_of_changeovers = int(re.sub('[^\d]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[6]/text()'))))

        if number_of_changeovers > 1:

            stops = 1

        else:

            stops = 0
        # 6am - 9am | 4pm-7pm
        time = int(kb.get_time(kb))
        if ((time >= 600) & (time <= 900) or ((time >= 1600) & (time <= 1900))):

            time = 1

        else:

            time = 0

        if departing_station == 'acle':
            routeInformation = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                         [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
                                         [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                         [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1],
                                         [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],
                                         [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1],
                                         [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
                                         [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
            routeLate = np.array([[0, 0, 0, 1, 0,
                                   0, 1, 0, 1, 1,
                                   1, 1, 1, 0, 0,
                                   1, 0, 0, 1, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 1, 1, 0,
                                   0, 1, 0, 0, 1,
                                   1, 0, 1, 0, 0]]).T

            delayTimes = {5, 2, 7, 1, 7, 11, 2, 3, 1, 10, 8, 4, 6, 3, 2,
                          6, 3, 9, 6, 1, 2, 8, 17, 5, 2, 4, 1, 7, 3, 6, 4,
                          8, 12, 6, 7, 2, 12, 3, 6, 1, 5, 8, 6, 14, 5, 6, 2}

        elif departing_station == 'attleborough':

            routeInformation = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                         [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
                                         [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                         [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1],
                                         [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],
                                         [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1],
                                         [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
                                         [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
            routeLate = np.array([[0, 0, 0, 0, 0,
                                   0, 1, 0, 0, 1,
                                   0, 1, 0, 0, 0,
                                   1, 0, 0, 1, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 1, 0,
                                   0, 1, 0, 0, 0,
                                   1, 0, 1, 0, 0]]).T

            delayTimes = {10, 2, 5, 8, 3, 12, 4, 5, 2, 2, 15, 35, 15, 3, 17, 31, 26,
                          4, 16, 4, 21, 4, 1, 4, 4, 6, 3, 7, 6, 4, 4, 7, 11, 5,
                          7, 2, 9, 4, 1, 1, 2, 1, 4, 2, 5}

        elif departing_station == 'beccles':

            routeInformation = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                         [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
                                         [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                         [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1],
                                         [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],
                                         [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1],
                                         [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
                                         [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
            routeLate = np.array([[0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 1, 0, 0, 0,
                                   1, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 1, 0,
                                   1, 0, 0, 0, 0]]).T

            delayTimes = {1, 3, 3, 6, 2, 3, 4, 8, 1, 3, 6, 3, 9, 12, 3, 8, 10, 3, 1,
                          6, 8, 4, 8, 2, 6, 4, 7, 4, 2, 7, 5, 3, 9, 10, 3, 9,
                          4, 6, 13, 6, 5, 4, 8, 8, 5, 7, 4, 4, 2, 5, 6, 6, 2}

        elif departing_station == 'cambridge':

            routeInformation = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                         [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
                                         [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                         [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1],
                                         [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],
                                         [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1],
                                         [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
                                         [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
            routeLate = np.array([[0, 1, 1, 0, 0,
                                   1, 1, 1, 0, 0,
                                   0, 1, 1, 1, 0,
                                   1, 1, 1, 0, 1,
                                   0, 1, 0, 0, 1,
                                   1, 0, 0, 1, 0,
                                   0, 1, 0, 0, 0,
                                   0, 0, 0, 1, 1]]).T

            delayTimes = {12, 4, 6, 2, 5, 8, 7, 4, 6, 5, 3, 4, 4, 10, 5, 9,
                          2, 20, 8, 14, 6, 12, 10, 8, 5, 3, 6, 13, 8, 16, 5,
                          8, 4, 2, 10, 4, 16, 5, 8, 9, 6, 2, 6, 3, 6, 3, 8, 10}

        elif departing_station == 'diss':

            routeInformation = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                         [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
                                         [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                         [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1],
                                         [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],
                                         [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1],
                                         [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
                                         [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
            routeLate = np.array([[1, 1, 0, 0, 0,
                                   0, 1, 1, 1, 0,
                                   0, 1, 0, 1, 1,
                                   1, 0, 0, 0, 1,
                                   0, 0, 0, 0, 1,
                                   1, 1, 0, 0, 0,
                                   0, 0, 0, 1, 1,
                                   0, 1, 0, 0, 0]]).T

            delayTimes = {9, 4, 8, 7, 9, 1, 7, 8, 5, 9, 3, 2, 10, 4, 6, 4,
                          18, 22, 2, 13, 4, 8, 2, 9, 6, 7, 3, 5, 12, 6, 5, 4, 9,
                          4, 9, 9, 4, 4, 1, 4, 5, 7, 8, 4, 2, 3, 3, 6, 1, 3}

        elif departing_station == 'ipswich':

            routeInformation = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                         [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
                                         [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                         [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1],
                                         [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],
                                         [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1],
                                         [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
                                         [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
            routeLate = np.array([[0, 1, 0, 0, 0,
                                   0, 1, 1, 0, 0,
                                   0, 1, 0, 1, 0,
                                   0, 0, 1, 0, 1,
                                   0, 0, 0, 0, 0,
                                   0, 1, 0, 0, 0,
                                   0, 0, 0, 1, 0,
                                   0, 1, 0, 1, 0]]).T

            delayTimes = {4, 6, 2, 8, 5, 12, 8, 4, 6, 3, 10, 5, 5, 4, 8, 2, 7,
                          4, 8, 1, 21, 8, 10, 4, 6, 9, 3, 10, 4, 8, 22, 13, 10,
                          4, 9, 10, 6, 2, 7, 4, 9, 5, 5}

        elif departing_station == 'norwich':

            routeInformation = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                         [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
                                         [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                         [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1],
                                         [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],
                                         [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1],
                                         [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
                                         [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
            routeLate = np.array([[0, 1, 1, 1, 0,
                                   0, 0, 1, 1, 0,
                                   0, 1, 0, 1, 0,
                                   1, 0, 1, 0, 1,
                                   0, 1, 0, 0, 0,
                                   0, 0, 1, 1, 0,
                                   1, 1, 0, 0, 1,
                                   1, 1, 0, 1, 0]]).T

            delayTimes = {3, 8, 5, 17, 13, 5, 9, 5, 8, 10, 5, 2, 2, 3, 2, 6,
                          4, 9, 10, 3, 2, 3, 8, 10, 3, 6, 8, 8, 6, 5, 7, 3, 12,
                          10, 5, 3, 2, 2, 8, 4, 7, 2, 9, 5, 14, 9, 3, 12, 10}

        elif departing_station == 'peterborough':

            routeInformation = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                         [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
                                         [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                         [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1],
                                         [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],
                                         [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1],
                                         [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
                                         [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
            routeLate = np.array([[0, 1, 1, 1, 0,
                                   0, 0, 1, 1, 0,
                                   1, 1, 0, 1, 0,
                                   1, 1, 1, 0, 1,
                                   0, 1, 0, 0, 1,
                                   0, 0, 0, 1, 0,
                                   0, 1, 0, 0, 1,
                                   1, 0, 1, 1, 0]]).T

            delayTimes = {6, 2, 9, 14, 10, 4, 8, 9, 4, 6, 1, 1, 7, 3, 2, 9, 5,
                          8, 14, 9, 10, 4, 6, 8, 3, 2, 6, 9, 13, 5, 2, 6, 4,
                          9, 5, 6, 4, 9, 2, 3, 9, 6, 4, 5, 1, 7, 4, 12, 6}

        trainPredictions.weightAdjustment(routeInformation, routeLate, 15000)

        prediction = trainPredictions.prediction(np.array([day, stops, time]))
        percentage = prediction * 100
        print("There is up to a ", percentage, "% chance that your train will be delayed")

        predictedDelay = trainPredictions.timeMean(delayTimes)
        print("Your predicted train delay is ", predictedDelay, " minutes, should one occur.")


if __name__ == "__main__":
    kb = KnowledgeBase
    pm = PredictionModel
    test_bot = GAChatBot()
    test_bot.__init__()
    test_bot.run_bot()
