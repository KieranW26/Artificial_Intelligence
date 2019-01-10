# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:43:51 2018

@author: ging3
"""
from datetime import time
from datetime import datetime
import re
import csv 

class GACHATBOT:
    
    kb_from_station_name = "empty"
    kb_to_station_name = "empty"
    
    kb_from_station_code = ""
    kb_to_station_code = ""
    
    #GETS TODAY DATE AND TIME AND SEPERATES THEM
    d = datetime.now().strftime("%Y-%m-%d %H:%M")
    kb_date, space, kb_time = d.partition(' ')
   # kb_date, space, kb_time = d.partition(' ')
    dflag = 0
    tflag = 0
    
    kb_return = False
    kb_ret_date, space2, kb_ret_time = d.partition(' ')
    
    #kb_ret_date, space2, kb_ret_time = d.partition(' ') 
    kb_command = '' 
    
    cb_flag = 0
    cb_running = True
    
    

   
    
    #Key Words and Phrases  
    TRAIN_STATIONS = ["diss", "norwich"]
   # data = csv.reader(open("norfolk_stations.csv"))
    #for line in data:
     #   TRAIN_STATIONS.append(re.sub(r'[^a-zA-Z0-9 ]+', '', str(line).lower()))
      #  print(line)
        
    OPENING_PHRASES = ("Hello, I am TrainBot how could I help?")
    MONTHS = ("january","february","march", "april", "may", "june", "july", "august", "september", "october", "november" , "decemeber")
    TIME_CONTAIN = ("am" , "pm")
    
    #REGEX 
    DATE_REGEX = ('\d{2}/\d{2}/\d{4}')
    TIME_REGEX = ('^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')

  
    
    
    def runBot(self): 
        while self.cb_running is True :
            
            print( self.kb_from_station_name, self.kb_to_station_name, self.kb_date, self.kb_time, self.kb_return  )
            if self.kb_return is True:
                print(self.kb_ret_date, self.kb_ret_time)
            userInput = input("USER: ")
           # print(self.DATE)
            #self.DATE = self.DATE.replace(year = 2017, hour = 13)
            #print(self.DATE)
            if userInput == "stop":
                self.cb_running = False
            else: 
                
                if self.cb_flag == 1: 
                    print("")
                    if "yes" in userInput: 
                        # WHERE THE PROGRAM CALLS THE FIND TRAIN TICKET FUNCTION
                        # RENAME IF NEEDED - JACK
                        self.findTrainTimes()
                        self.kb_from_station_name = "empty"
                        self.kb_to_station_name = "empty" 
                        self.kb_date, self.space, self.kb_time = self.d.partition(' ')
                        self.kb_return = False 
                        self.kb_ret_date, self.space, self.kb_time = self.d.partition(' ')
                        self.cb_flag = 0
                        self.dflag = 0
                        self.tflag = 0
                    else:
                        self.kb_from_station_name = "empty"
                        self.kb_to_station_name = "empty" 
                        self.kb_date, self.space, self.kb_time = self.d.partition(' ')
                        self.kb_return = False 
                        self.kb_ret_date, self.space, self.kb_time = self.d.partition(' ')
                        self.cb_flag = 0
                        self.dflag = 0
                        self.tflag = 0 
                        print("okay, lets try that again, what is your journey?")
                else: 
                    self.listen(userInput)
                    self.respond(userInput)
            


    def listen(self, sentence): 
        words = sentence.split()
        if "return" in sentence.lower(): 
            self.kb_return = True
        for counter, word in enumerate(words):
           
            if word.lower() in self.TRAIN_STATIONS:
                if words[counter-1] is "to" or self.kb_from_station_name is not "empty":
                    self.kb_to_station_name = word.lower()
                else:
                    self.kb_from_station_name = word.lower() 
                    print(self.kb_from_station_name)
                    #date capture - only 1 method implemented with format "dd/mm/yy"
            elif re.search(self.DATE_REGEX, word) and self.dflag == 0:
                self.dflag = 1
                self.kb_date = word
            elif  re.search(self.TIME_REGEX, word) and self.tflag == 0:
                self.tflag = 1
                self.kb_time = word         
            elif self.kb_return is True: 
                if re.search(self.DATE_REGEX, word):
                    self.kb_ret_date = word
                elif re.search(self.TIME_REGEX, word):
                    self.kb_ret_time = word
                
      
            
    
    def respond(self, setence):
        start = "BOT: " 
        answer = "You still need to enter your" 
        if self.kb_from_station_name == "empty":
            answer = answer + " starting station " 
        if self.kb_to_station_name == "empty":
            if answer == "You still need to enter your":
                answer = answer + " destination station "
            else: 
                answer = answer + "and destination station"
        
        #checks if they still need minimum information 
        if answer != "You still need to enter your":
            print(start + answer )
        else: 
            response = "You are traveling from " + self.kb_from_station_name + " to " + self.kb_to_station_name + " on " 
            response = response + self.kb_date + " at " +  self.kb_time
            
            if self.kb_return:
                response = response + " and returning on the " 
                if self.kb_ret_date == self.kb_date:
                    response = response + " same day at " + self.kb_ret_time
                else:
                    response = response + self.kb_ret_date + " at " + self.kb_ret_time
            print(response + ". Is that Correct?")
            self.cb_flag +=1
   
    
    def findTrainTimes(self):
        
        print("") 
    
     
          
   



TestChatBot = GACHATBOT()
TestChatBot.runBot()




