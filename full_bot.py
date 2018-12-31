# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:43:51 2018

@author: ging3
"""
import csv
from datetime import time
from datetime import datetime
import calendar
import re
import re
from typing import Tuple
from urllib.request import urlopen
from lxml import html
import requests
from pyknow import *



class GACHATBOT:
    # Variables for Journey
    START_STATION = "empty"
    DESTINATION_STATION = "empty"
    DATE = datetime.today()
    # Variables for return journeys
    RETURN = False
    RETURN_DATE = datetime.today()
    # Variables for running of the system
    RUNNING = True
    CHECK_DATE = datetime.today()
    FLAG = 0



    # Key Words and Phrases


    data = csv.reader(open("norfolk_stations.csv"))
    TRAIN_STATIONS = []
    for line in data:
        TRAIN_STATIONS.append(re.sub(r'[^a-zA-Z0-9 ]+', '', str(line).lower()))

    OPENING_PHRASES = ("Hello, I am TrainBot how could I help?")
    MONTHS = (
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
    "decemeber")
    TIME_CONTAIN = ("am", "pm")

    # REGEX
    DATE_REGEX = ('\d{2}/\d{2}/\d{4}')
    TIME_REGEX = ('^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')

    def runBot(self):
        while self.RUNNING is True:
            userInput = input("USER: ")
            # print(self.DATE)
            # self.DATE = self.DATE.replace(year = 2017, hour = 13)
            # print(self.DATE)
            if userInput == "stop":
                self.RUNNING = False
            else:

                if self.FLAG == 1:
                    print("Sup")
                    if "yes" in userInput:
                        self.findTrainTimes()
                    else:
                        self.clear()
                        self.listen(userInput)
                        self.respond(userInput)
                else:
                    self.listen(userInput)
                    self.respond(userInput)

    def listen(self, sentence):
        words = sentence.split()
        if "return" in sentence.lower():
            self.RETURN = True
        for counter, word in enumerate(words):

            if word.lower() in self.TRAIN_STATIONS:
                if words[counter - 1] is "to" or self.START_STATION is not "empty":
                    self.DESTINATION_STATION = word.lower()
                    print(self.DESTINATION_STATION)
                else:
                    self.START_STATION = word.lower()
                    print(self.START_STATION)
                    # date capture - only 1 method implemented with format "dd/mm/yy"
            elif re.search(self.DATE_REGEX, word):
                sday, smonth, syear = word.split("/")
                self.DATE = self.DATE.replace(day=int(sday), month=int(smonth), year=int(syear))
            elif re.search(self.TIME_REGEX, word):
                hh, mm = word.split(":")
                print(hh)
                self.DATE = self.DATE.replace(hour=int(hh), minute=int(mm))
                print(self.DATE)
            elif self.RETURN is True:
                if re.search(self.DATE_REGEX, word):
                    sday, smonth, syear = word.split("/")
                    self.DATE = self.RETURN_DATE = datetime.replace(day=int(sday), month=int(syear), year=int(syear))
                elif re.search(self.TIME_REGEX, word):
                    hh, mm = word.split(":")
                    self.DATE = self.DATE.replace(hour=int(hh), minute=int(mm))

    def respond(self, setence):
        start = "BOT: "
        answer = "You still need to enter your"
        if self.START_STATION == "empty":
            answer = answer + " starting station "
        if self.DESTINATION_STATION == "empty":
            if answer == "You still need to enter your":
                answer = answer + " destination station "
            else:
                answer = answer + "and destination station"

        # checks if they still need minimum information
        if answer != "You still need to enter your":
            print(start + answer)
        else:
            response = "You are traveling from " + self.START_STATION + " to " + self.DESTINATION_STATION + " on "
            response = response + str(self.DATE.day) + "/" + str(self.DATE.month) + "/" + str(self.DATE.year) + " at "
            response = response + str(self.DATE.hour) + ":" + str(self.DATE.minute)
            if self.RETURN:
                response = response + " and returning on the "
                if self.RETURN_DATE.month == self.DATE.month and self.RETURN_DATE.day == self.DATE.day:
                    response = response + "same day at"
                else:
                    response = response + str(self.DATE.day) + "/" + str(self.DATE.month) + "/" + str(self.DATE.year)
            print(response + ". Is that Correct?")
            self.FLAG += 1

    def findTrainTimes(self):
        class TrainTickets(KnowledgeEngine):
            @DefFacts()
            def _initial_action(self):
                yield Fact(action="route")

            @Rule(Fact(action='route'),
                  Fact(departing_station=MATCH.departing_station),
                  Fact(arriving_station=MATCH.arriving_station),
                  Fact(time=MATCH.time),
                  Fact(date=MATCH.date))
            def route(self, departing_station, arriving_station, time, date):
                time = str(time)
                url = "https://traintimes.org.uk/" + str(departing_station) + "/" + str(arriving_station) #+ "/" \
                      #+ time + "/" + str(date)
                print(url)
                page = requests.get(url)
                tree = html.fromstring(page.content)
                if 'a' in time:
                    time = time.replace('a', '')
                    date = str(date)
                    print(departing_station + ' to ' + arriving_station + ' arriving at ' + time + ' on ' + date)
                else:
                    print(departing_station + ' to ' + arriving_station + ' departing at ' + time + ' on ' + date)
                for x in range(5):
                    printout = ''
                    times = tree.xpath('//li[@id="result' + str(x) + '"]/strong[1]/text()')
                    printout = printout + re.sub('[\[\'\]' ']', '', str(times))
                    platform_temp = tree.xpath('//li[@id="result' + str(x) + '"]/small/em/text()')
                    platform_temp = str(platform_temp).replace('\\n', '').replace('\\t', '').replace('Platform',
                                                                                                     'Platform ') \
                        .replace(';', ' ')
                    platform = re.sub('[^a-zA-Z\d\s:]', '', str(platform_temp))
                    if platform_temp:
                        printout = printout + ' ' + platform + ' '
                    else:
                        printout = printout + '             '
                    price = tree.xpath('//li[@id="result' + str(x) + '"]/small[2]/span[@class="tooltip" and 1]/text()')
                    printout = printout + re.sub('[\[\'\]' ']', '', str(price))
                    print(printout)

        engine = TrainTickets()
        engine.reset()  # Prepare the engine for the execution.
        engine.declare(Fact(departing_station=self.START_STATION))
        engine.declare(Fact(arriving_station=self.DESTINATION_STATION))
        engine.declare(Fact(time=time))
        engine.declare(Fact(date=self.DATE))
        engine.run()  # Run it!

    def clear(self):
        self.START_STATION = "empty"
        self.DESTINATION_STATION = "empty"
        self.DATE = datetime.today()
        self.RETURN = False
        self.RETURN_DATE = datetime.today()
        self.FLAG = 0


TestChatBot = GACHATBOT()
TestChatBot.runBot()




