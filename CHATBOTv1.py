# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:43:51 2018

@author: ging3
"""
from datetime import time
from datetime import datetime
import calendar 
import re


class GACHATBOT: 
    #Variables for Journey
    START_STATION = "empty"
    DESTINATION_STATION = "empty" 
    DATE = datetime.today()
    #Variables for return journies
    RETURN = False 
    RETURN_DATE = datetime.today()
    #Variables for running of the system
    RUNNING = True
    CHECK_DATE = datetime.today() 
    FLAG = 0
   
    
    #Key Words and Phrases  
    TRAIN_STATIONS = ("norwich", "diss" ,
                  "stowmarket", "bury" , "cambrdige")
    OPENING_PHRASES = ("Hello, I am TrainBot how could I help?")
    MONTHS = ("january","february","march", "april", "may", "june", "july", "august", "september", "october", "november" , "decemeber")
    TIME_CONTAIN = ("am" , "pm")
    
    #REGEX 
    DATE_REGEX = ('\d{2}/\d{2}/\d{4}')
    TIME_REGEX = ('^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    
    def runBot(self): 
        while self.RUNNING is True :
            userInput = input("USER: ")
           # print(self.DATE)
            #self.DATE = self.DATE.replace(year = 2017, hour = 13)
            #print(self.DATE)
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
                if words[counter-1] is "to" or self.START_STATION is not "empty":
                    self.DESTINATION_STATION = word.lower() 
                    print(self.DESTINATION_STATION)
                else:
                    self.START_STATION = word.lower() 
                    print(self.START_STATION)
                    #date capture - only 1 method implemented with format "dd/mm/yy"
            elif re.search(self.DATE_REGEX, word):
                sday, smonth, syear = word.split("/")      
                self.DATE = self.DATE.replace(day = int(sday), month = int(smonth), year = int(syear))
            elif  re.search(self.TIME_REGEX, word):
                hh, mm = word.split(":")
                print(hh)
                self.DATE = self.DATE.replace(hour=int(hh), minute=int(mm))
                print(self.DATE)
            elif self.RETURN is True: 
                if re.search(self.DATE_REGEX, word):
                    sday, smonth, syear = word.split("/")
                    self.DATE = self.RETURN_DATE = datetime.replace(day = int(sday), month = int(syear), year = int(syear))
                elif re.search(self.TIME_REGEX, word):
                     hh, mm = word.split(":")
                     self.DATE = self.DATE.replace(hour = int(hh), minute = int(mm))
                    
                
      
            
    
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
        
        #checks if they still need minimum information 
        if answer != "You still need to enter your":
            print(start + answer )
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
            self.FLAG +=1
   
    
    def findTrainTimes(self):
        #code for gathering train times here 
        print("") 
    
    def clear(self):
        self.START_STATION = "empty"
        self.DESTINATION_STATION = "empty" 
        self.DATE = datetime.today()
        self.RETURN = False 
        self.RETURN_DATE = datetime.today()
        self.FLAG = 0




TestChatBot = GACHATBOT()
TestChatBot.runBot()




