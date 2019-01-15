# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:43:51 2018
@author: ging3
"""
from lxml import html
from datetime import time, date
from datetime import datetime
from string import Template
import re
import csv
import requests
import nltk 

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
        self.kb_from_station_name = ""
        self.kb_to_station_name = ""
        self.kb_from_station_code = ""
        self.kb_to_station_code = ""
        self.kb_date = ""
        self.kb_time = ""
        self.kb_depart_or_arrive = ""
        self.kb_ret_date = ""
        self.kb_ret_time = ""
        self.kb_ret_depart_or_arrive = ""
        self.kb_command = ""


class GAChatBot:
    #!! REGEX !!# 
    #Templates
    bot_template = Template("BOT: $message")
    
    date_error = False;
    
    stations = ["norwich" , "diss", "stowmarket"]
    date_regex = ('\d{2}/\d{2}/(?:\d{2}){1,2}')
    time_regex = ('^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    month = ("(?:jan(?:uary)?)|(?:feb(?:ruary)?)|(?:mar(?:ch)?)|(?:apr(?:il)?)|(?:may?)"
    + "|(?:jun(?:e)?)|(?:jul(?:ly)?)|(?:aug(?:ust)?)|(?:sep(?:tember)?)|(?:oct(?:ober)?)|(?:nov(?:ember)?)" 
    + "|(?:dec(?:ember)?)") 
    ret = False;
    def setUp(self):        
        posts = nltk.corpus.nps_chat.xml_posts()[:10000]
        featuresets = [(self.meaning(post.text), post.get('class'))
                for post in posts]
        size = int(len(featuresets) * 0.1)
        train_set = featuresets[size:]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier
    
    def meaning(self, post):
        features = {}
        for word in nltk.word_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features
    
    def run(self, classifier): 
        running = True 
        print(self.bot_template.substitute(message="Hello There, how can i help you today?"))
        while running: 
            user_input = input("USER: ")
            if user_input == "stop":
                running = False
            elif user_input == "clear":
                kb.clear_kb(kb) 
                print("BOT: Data Clear" )
            else:
                self.listen(classifier, user_input)
            

    def listen(self, classifier, user_input): 
        intent = classifier.classify(self.meaning(user_input)) 
        if intent == "ynQuestion":
            self.ynQuestion(user_input)
        elif intent == "whQuestion": 
            self.whQuestion(user_input)
        elif intent == "Greet":
            print((self.bot_template.substitute(message="Hiya!")))
        else: 
            self.trains(user_input)
    def ynQuestion(self, user_input):
        print("no answer for the question sorry")
        
    def whQuestion(self, user_input):
        if re.search("delay", user_input.lower()):
            stations = []
            for word in user_input.split():
                if word.lower in self.stations:
                    stations.append(word)
            if not stations: 
                print("To determine if there was a delay, I will need the two stations")
            elif len(stations) == 1: 
                print("We got one of your stations, but will need the other one to continue")
            else:
                print("we got em")
                
    
        
    def trains(self, user_input):        
        words = user_input.split()  
        sta = []
        dates = []
        times = [] 
        count = 0
        times = re.findall(self.month, user_input)
        for counter, word in enumerate(words):
               if word.lower() in self.stations:
                   sta.append(word)
               elif re.search(self.date_regex, word):
                   dates.append(word)
                   print(word)
               elif re.match(self.month, word):
                   print(word)
                   #dates.append(self.convertDate(user_input, word, count))
                   count ++ 1
               elif re.search(self.time_regex, word):
                   times.append(word)
               elif word.lower() == "return" :
                   self.ret = True

        if dates: 
            self.analyseDates(words, dates)
        if times:
            self.analyseTimes(words, times)
        if sta:
            self.analyseStations(words, sta)
        if sta or times or dates: 
            self.trainResponse()
        else: 
            print("BOT: Not sure what you meant by that, do you want to book a train perhaps?")
    
  
    def convertDate(self, date, word, count):
        day = re.findall('\d+(?=st|nd|rd|th)', date)
        if len(day[count]) == 1:
            day[count] = "0" + day[count]
        month = str(self.monthToNumber(word))
        if len(month) == 1:
            month = "0" + month
        year = re.findall('(?<=\s)[0-9]{4}', date)
        if year and len(year[count]) == 4:  
            year[count] = year[count][-2:]
        newDate = day[count] + "/" + month + "/"
        if year:
            return(newDate + year[count])
        else: 
            return(newDate + "19")
        
        
        
    #analysing stations
    def analyseStations(self, words, stations):
        if len(stations) == 1: 
            if len(words) != 1:
                print(stations[0])
                x = words.index(stations[0])
                if words[x-1].lower() == "to":
                    kb.set_to_station(kb, stations[0])
                    print(stations[0])
                else:
                    kb.set_from_station(kb, stations[0])
                    print(stations[0])
            else:
                kb.set_from_station(kb, stations[0])
                print(stations[0])
        else: 
            start = stations[1]
            finish = stations[0]
            temp = ""
            x = words.index(start)
            y = words.index(finish)
            if words[x-1].lower() == "to" or words[y-1].lower() == "from":
                temp = start
                start = finish 
                finish = temp
            kb.set_from_station(kb, start.lower())
            kb.set_to_station(kb, finish.lower())
            print(kb.kb_from_station_name)
            print(kb.kb_to_station_name)
            #self.findTrainTimes()
        
    #analysing dates
    def analyseDates(self, words, dates):
        date1 = datetime.strptime(dates[0], '%d/%m/%y')
        #compare date needs to be made at begining of the run of the program
        if self.compareDates(datetime.now(), date1):
            self.date_error = True 
        elif len(dates) > 1:
            date2 = datetime.strptime(dates[1], '%d/%m/%y')
            if self.compareDates(date1, date2):
                print(str(date1) + " is earlier than " + str(date2))
                kb.set_date(kb, dates[1])
                kb.set_return_date(kb, dates[0])
            else: 
                print(str(date1) + " is later than " + str(date2))
                kb.set_date(kb, dates[0].lower())
                kb.set_date(kb, dates[1].lower())
                print(kb.kb_ret_date)
        else: 
            kb.set_date(kb, dates[0].lower())
             
    def analyseTimes(self, words, times): 
        if len(times) == 1: 
            if self.ret: 
                kb.set_time(kb, times[0])
        else: 
            kb.set_time(kb, times[1])
            kb.set_time(kb, times[0])
            
    def compareDates(self, date1, date2): 
        return date1 > date2
    
    def trainResponse(self):
        answer = "We need your "   
        if kb.kb_to_station_name == "":
            print("BOT: You told me your start station," + str(kb.kb_from_station_name) + ", so where are you going?")
            flag = 0
            while kb.kb_to_station_name == "" and flag != 1: 
                user_input = input("USER: ")
                intent = self.listenForStation(user_input)
                if intent == "Accept" or intent == "yAnswer": 
                    print("Okay, please can you type in your destination")
                elif intent == "Reject" or intent == "nAnswer": 
                    print("Ah okay, my mistake, how could I help you?")
                    flag = 1
        elif kb.kb_from_station_name == "": 
            print("BOT: You only told your destination, so where do you want to start your journey")
            flag = 0
            while kb.kb_from_station_name == "" and flag != 1: 
                user_input = input("USER: ")
                intent = self.listenForStation(user_input)
                if intent == "Accept" or intent == "yAnswer": 
                    print("Okay, please can you type in your destination")
                elif intent == "Reject" or intent == "nAnswer": 
                    print("Ah okay, my mistake, how could I help you?")
                    flag = 1
        print("BOT: All good, I got your data you are going from " + str(kb.kb_from_station_name) + " to " + kb.kb_to_station_name)
        
        
    def listenForStation(self, user_input):
      words = user_input.split()  
      stations = []
      for word in words: 
          if word.lower() in self.stations:
              stations.append(word)
      print(stations)
      if stations: 
          if len(stations) > 1: 
              #print("Whoops")
              print("BOT: Too Many Stations")
              return "return"
          elif kb.kb_from_station_name == "":
              #print("fROM STATION")
              station = stations[0]
              kb.set_from_station(kb, station)
          else:
              #print("to station")
              kb.set_to_station(kb, stations[0])
          return           
      else: 
          print("BOT: Wait, do you not wish to book a train?")
          user_input = input("USER:")
          return self.determineIntent(user_input)
      
    def determineIntent(self, user_input):       
        intent = classifier.classify(self.meaning(user_input)) 
        return intent
          
    def monthToNumber(self, string):
        m = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr':4,
             'may':5,
             'jun':6,
             'jul':7,
             'aug':8,
             'sep':9,
             'oct':10,
             'nov':11,
             'dec':12
            }
        s = string.strip()[:3].lower()
    
        try:
            out = m[s]
            return out
        except:
            raise ValueError('Not a month')
    
    def compareTime(self, time1, time2): 
        return time1 > time2
    
  
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
    classifier = test_bot.setUp()
    test_bot.run(classifier)