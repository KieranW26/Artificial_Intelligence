# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:43:51 2018
@author: ging3
"""
from lxml import html
from datetime import time, date
from datetime import datetime, timedelta
from string import Template
import re
import csv
import requests
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize



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
    stemmer = PorterStemmer() 
    bot_template = Template("BOT: $message")
    
    response_template = Template("BOT: So you are planning to journey from $station1 to $station2")
    date_error = False;
    
    stations = ["norwich" , "diss", "stowmarket"]
    
    date_regex = ('\d{2}/\d{2}/(?:\d{2}){1,2}')
    time_regex = ('^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    month = ("(?:jan(?:uary)?)|(?:feb(?:ruary)?)|(?:mar(?:ch)?)|(?:apr(?:il)?)|(?:may?)"
    + "|(?:jun(?:e)?)|(?:jul(?:ly)?)|(?:aug(?:ust)?)|(?:sep(?:tember)?)|(?:oct(?:ober)?)|(?:nov(?:ember)?)" 
    + "|(?:dec(?:ember)?)") 
    
    longMonth = [1, 3, 5, 7, 8, 10, 12]
    shortMonth = [4, 6, 9, 11]
    dayTerms = ["today","tomorrow", "week", "fortnight" , "fortnight"]
    dayTerms2 = ["first", "second", "third" , "fourth" , "fifth" 
                 "sixth", "seventh", "eighth", "ninth", "tenth" 
                 "eleventh", "twelveth", "thirteenth", "fourteenth" 
                 "fifteenth", "sixteenth", "eighteenth", "nineteenth" 
                 "twentieth", "twenty-first", "twenty-second", "twenty-fourth"
                 "twenty-fifth", "twenty-sixth", "twenty-seventh", "twenty-eighth" 
                 "twenty-ninth", "thirtieth", "thirty-first"]
                
    delayTerms = ["delay", "late" , "interupt"]
    everything = ["everything", "all", "none"]
    
    ret = False
    confirmed = False
    delay = False
    invalidDate = False
    
    
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
                print("BOT: Good-bye, I hope I've been helpful")
            elif user_input == "clear":
                kb.clear_kb(kb) 
                print("BOT: Data Clear" )
            else:
                self.listen(classifier, user_input)
            

    def listen(self, classifier, user_input): 
        intent = classifier.classify(self.meaning(user_input)) 
        dates, times, sta, words = self.gatherData(user_input)
        if dates: 
            self.analyseDates(words, dates)
        if times:
            self.analyseTimes(words, times)
        if sta:
            self.analyseStations(words, sta)
        if dates or times or sta:
            self.validData()
            
        elif intent == "ynQuestion":
            self.ynQuestion(user_input)
        elif intent == "whQuestion": 
            self.whQuestion(user_input)
        elif intent == "Greet":
            print((self.bot_template.substitute(message="Hiya!")))
        elif intent == "Reject" or intent == "nAnswer":
            print("BOT: Okay so we won't do that")
        elif intent == "Agree" or intent == "yAnswer": 
            print("BOT: Glad we are both of the same page")
        else:
            print("BOT: Not sure if I understand you")
                
    def ynQuestion(self, user_input):
        print("no answer for the question sorry")
        
    def whQuestion(self, user_input):
        print("Whats up")
    
        
    def gatherData(self, user_input):
        user_input = user_input.replace(',', '')
        words = user_input.split()  
        sta = []
        dates = []
        times = [] 
        count = 0
        times = re.findall(self.month, user_input)
        for counter, word in enumerate(words):
               #print(self.stemmer.stem(word))
               
               if word.lower() in self.stations:
                   sta.append(word)
               elif re.search(self.date_regex, word):
                   dates.append(word)
                   #print(word)
               elif re.match(self.month, word):
                   print(word)
                   newDate = self.convertDate(user_input, word, words, count)
                   if newDate != "Not valid":
                       count = count + 1
                       dates.append(newDate)
               elif re.search(self.time_regex, word):
                   times.append(word)
               elif self.stemmer.stem(word) == "return" or self.stemmer.stem(word) == "back":
                  self.ret = True
               elif self.stemmer.stem(word) in self.dayTerms:
                   dates.append(self.termToDate(self.stemmer.stem(word)))
               elif self.stemmer.stem(word) in self.delayTerms:
                   self.delay = True
        
        if dates: 
            self.analyseDates(words, dates)
        if times:
            self.analyseTimes(words, times)
        if sta:
            self.analyseStations(words, sta)
        
        return dates, times, sta, words
       
    
  
    def convertDate(self, user_input, word, words, count):
        
        day = re.findall('\d+(?=st|nd|rd|th)', user_input)
        if not day:
            for word in words: 
               if word.lower() in self.dayTerms2:
                    day.append(self.dayTerms2.index(word.lower()))
        if not day: 
            return "Not valid" 
        month = str(self.monthToNumber(word))
        
        if len(month) == 1:
            month = "0" + month
       
        newDate = day[count] + "/" + month + "/"    
       
        return(newDate + "19") 

        
        
        
    #analysing stations
    def analyseStations(self, words, stations):
        if len(stations) == 1: 
            if len(words) != 1:
                x = words.index(stations[0])
                if words[x-1].lower() == "to":
                    kb.set_to_station(kb, stations[0])
                else:
                    kb.set_from_station(kb, stations[0])
         
            else:
                kb.set_from_station(kb, stations[0])
              
        else: 
            start = stations[1]
            finish = stations[0]
            temp = ""
            x = words.index(start)
            y = words.index(finish)
            if len(words) > 1:    
                if words[x-1].lower() == "to" or words[y-1].lower() == "from":
                    temp = start
                    start = finish 
                    finish = temp
            kb.set_from_station(kb, start.lower())
            kb.set_to_station(kb, finish.lower())

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
                kb.set_date(kb, dates[1])
                kb.set_return_date(kb, dates[0])
            else: 
                kb.set_date(kb, dates[0])
                kb.set_return_date(kb, dates[1])
        else: 
            if kb.kb_date != "": 
                kb.set_return_date(kb, dates[0])
            else:
                kb.set_date(kb, dates[0])
             
    def analyseTimes(self, words, times): 
        if len(times) == 1: 
            kb.set_time(kb, times[0])
        
        else: 
            kb.set_time(kb, times[1])
            kb.set_ret_time(kb, times[0])
            
    def compareDates(self, date1, date2): 
        return date1 > date2
    
    def validData(self):
        if self.delay == True: 
            print("Hes looking for a delay")
        if kb.kb_to_station_name == "":
            print("BOT: Okay, so what is your destination?")
            flag = 0
            while kb.kb_to_station_name == "" and flag != 1: 
                user_input = input("USER: ")
                intent = self.listenForStation(user_input)
                if intent == "Accept" or intent == "yAnswer": 
                    print("Okay, please can you type in your destination for this query")
                elif intent == "Reject" or intent == "nAnswer": 
                    print("Ah okay, my mistake, how could I help you?")
                    flag = 1
                elif intent == "None" :
                    flag = 1 
                
        if kb.kb_from_station_name == "": 
            print("BOT: And where are you travelling from ?")
            flag = 0
            while kb.kb_from_station_name == "" and flag != 1: 
                user_input = input("USER: ")
                intent = self.listenForStation(user_input)
                if intent == "Accept" or intent == "yAnswer": 
                    print("Okay, please can you type in your destination")
                elif intent == "Reject" or intent == "nAnswer": 
                    print("Ah okay, my mistake, how could I help you?")
                    flag = 1
        
        if self.delay == True:
            print(self.delayReply()) 
            x = self.confirm("chance of delay")
            if x == "True": 
                #callfunction
                print("x")
            self.confirmed = False
            
        else: 
            print(self.bookReply())
            self.confirm("ticket information")
            x = self.confirm("chance of delay")
            if x == "True": 
                print("x")
            self.confirmed = False
    
    def bookReply(self):
        response = self.response_template.substitute(station1 = kb.kb_from_station_name, station2 = kb.kb_to_station_name) 
        if kb.kb_date == "" :
            response = response + " today" 
        else: 
            response = response + " on the " + kb.kb_date 
        if kb.kb_time != "":
            response = response + " at " + kb.kb_time
        if self.ret == True:
            response = response + ". You will return "
            if kb.kb_ret_date == "":
                response = response +" later that day" 
            else: 
                response = response + "on " + kb.kb_ret_date
            if kb.kb_ret_time != "":
                response = response + " at " + kb.kb_ret_time 
            
        return response + ". Have I got that all right?"
        
        
            
    def delayReply(self):
        
        if kb.kb_date == "": 
            print("BOT: Which date do you want the prediction to be for?")
            flag = 0
            while kb.kb_date == "" and flag != 1: 
                user_input = input("USER: ")
                intent = self.listenForDates(user_input)
                if intent == "Accept" or intent == "yAnswer" or user_input.lower() == "yes": 
                    print("BOT: Alright, could you enter your date?")
                elif intent == "Reject" or intent == "nAnswer": 
                    print("BOT: Ah okay, my mistake")
                    flag = 1
        if kb.kb_time == "":
            flag = 0
            print("BOT: What time is the prediciton for?")
            while kb.kb_time == "" and flag != 1: 
                user_input = input("USER: ")
                intent = self.listenForDates(user_input)
                if intent == "Accept" or intent == "yAnswer" or user_input.lower() == "yes": 
                    print("BOT: Okay so you to contiue, please enter your time for the prediciton model")
                elif intent == "Reject" or intent == "nAnswer" or user_input.lower() == "no": 
                    print("BOT: Ah okay, my mistake lets go back to the beginning ")
                    flag = 1
        response = "BOT: Okay, so you want to know the chance of a delay between " + kb.kb_from_station_name + " to " + kb.kb_to_station_name + " on the " + kb.kb_date + " at " + kb.kb_time 
        return response + ". Is that correct?"
        

        
                    
    def confirm(self, query):
        while self.confirmed == False: 
            user_input = input("USER:")
            dates, times, sta, words = self.gatherData(user_input)
            intent = self.determineIntent(user_input)
            if intent == "yAnswer" or intent == "Agree" or user_input.lower() == "yes": 
                print("BOT: Alrighty, I shall retrieve the " + query)
                self.confirmed = True
                return "True"
            elif intent == "nAnswer" or intent == "Reject" or user_input.lower() == "no": 
                print("BOT: Okay what did i get wrong?")
                self.checkMistakes(user_input, dates, times, sta, query)     
            else:
                if dates or times or sta:
                    self.checkMistakes(user_input, dates, times, sta, query)
                else: 
                    print("BOT: I'm not sure what you want me to do")
        
    
    def checkMistakes(self, user_input, dates, times, sta, query):
        words = user_input.split()
        if dates: 
            if len(dates) > 1: 
                self.analyseDates(words, dates)
            elif self.ret == True: 
                if "return" in user_input: 
                    kb.set_date = dates[0]
                else: 
                    print("BOT: Which date is that? Is It the departure date or return date?")
                    user_input = input("USER: ")
                    intent = self.determineIntent(user_input)
                    if intent == "yAnswer" or intent == "Agree" or user_input.lower() == "yes" or user_input.lower() == "departure":
                        kb.set_date = dates[0]
                    elif intent == "nAnswer" or intent =="Reject" or user_input.lower() == "no" or user_input.lower() == "return":
                        kb.set_ret_date = dates[0]
                
                    
            else: 
                kb.set_date(kb, dates[0])
        if times: 
            if len(times) > 1: 
                self.analyseTimes(words, times)
               
            elif self.ret == True: 
                print("BOT: Is that the depature time or return time?")
                user_input = input("USER: ")
                intent = self.determineIntent(user_input)
                if intent == "yAnswer" or intent == "Agree" or user_input.lower() == "yes" or user_input.lower() == "departure":
                    kb.set_time = times[0]
                elif intent == "nAnswer" or intent =="Reject" or user_input.lower() == "no" or user_input.lower() == "return":
                    kb.set_ret_date = times[0]
            else: 
                kb.set_time(kb, times[0])

        if sta: 
            if len(sta) > 1: 
                self.analyseStations(words, sta)
            elif self.ret == True:
                if "return" in user_input: 
                    kb.set_to_station(sta[0])
                else:
                    print("BOT: Is that the depature or return station?")
                    user_input = input("USER: ")
                    intent = self.determineIntent(user_input)
                    if intent == "yAnswer" or intent == "Agree" or user_input.lower() == "yes" or user_input.lower() == "departure":
                        kb.set_time = sta[0]
                    elif intent == "nAnswer" or intent =="Reject" or user_input.lower() == "no" or user_input.lower() == "return":
                        kb.set_ret_date = sta[0]
            else: 
                kb.set_from_station_name(kb, sta[0])
        print(self.bookReply()) 
        self.confirm(query)
        
        
            
                
        
    def listenForStation(self, user_input):
      words = user_input.split()  
      stations = []
      for word in words: 
          if word.lower() in self.stations:
              stations.append(word)

      if stations: 
          station = stations[0]
          if len(stations) == 2: 
              self.analyseStations(words, stations)
              
          elif kb.kb_to_station_name == "":
              #print("to station")
              kb.set_to_station(kb, station)
              
          else:
              #print("fROM STATION")
              kb.set_from_station(kb, station)
              
          return           
      else: 
          print("BOT: Do you not wish to book a train?")
          user_input = input("USER:")
          return self.determineIntent(user_input)
      
    def listenForDates(self, user_input):
      words = user_input.split()  
      dates = []
      for word in words: 
          if self.stemmer.stem(word) in self.dayTerms:
              dates.append(self.termToDate(self.stemmer.stem(word)))
          elif re.search(self.date_regex, word):
              dates.append(word)
          elif re.search(self.dayTerms, word):
              dates.append(word)
      if dates: 
          kb.set_date(kb, dates[0])
          return("True")
      else: 
          print("BOT: I did not understand you there, do you wish to continue finding a delay prediction?")
          user_input = input("USER: ")
          return self.determineIntent(user_input)
      
      
    def listenForTimes(self, user_input):
         words = user_input.split()  
         times = []
         for word in words: 
             if re.search(self.time_regex, word):
                 times.append(word)
         if times: 
             kb.set_time(kb, times[0])
             return("True")
         else: 
             print("BOT: I did not understand you there, do you not wish to continue finding a delay prediction?")
             user_input = input("USER: ")
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
    def termToDate(self, string): 
        daysLater = self.termToNumber(string.lower())
        d = datetime.today() 
        d = d + timedelta(days=daysLater)
        return str(d.strftime('%d/%m/%y'))
        
    
    def termToNumber(self, string):
        n = {
             'today': 0,
            'tomorrow': 1,
             'week':7,
             'fortnight':14,
             'fort night':14,
            }
        try:
            out = n[string]
            return out 
        except:
            raise ValueError("Not a term")
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
    ps = PorterStemmer()
    example_words = ["Interuptions","delays","late","back","delay"]
    for w in example_words:
        print(ps.stem(w))
    test_bot = GAChatBot()
    classifier = test_bot.setUp()
    test_bot.run(classifier)