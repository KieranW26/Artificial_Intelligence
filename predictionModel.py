import numpy as np

class PredictionModel():
    
    def __init__(self):

        # generating the seed for the random number
        np.random.seed(1)       
        
        # coverting the weights, based on a 3 integer array representing information
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
    
    def trainData(self, trainDeparture):
        
         trainPredictions = PredictionModel()
         trainDeparture = str(input("What station are you departing from?: "))
         trainDeparture = trainDeparture.lower()
             
         trainDestination = str(input("What station is your destination?: "))
         trainDestination = trainDestination.lower()
            
         trainRoute = trainDeparture + " to " + trainDestination
            
         print("Your route is", trainRoute)
            
         dayOfTravel = str(input("What day are you travelling?: "))
         dayOfTravel = dayOfTravel.lower()
         if dayOfTravel == 'sunday' or 'saturday':
                
             day = 1
                
        else:
              
            day = 0
                     
        numberOfStops = int(input("How many stops are on your journey?: "))
        
        if numberOfStops > 1:
                
            stops = 1
                
        else:
                
            stops = 0
            
        timeOfDay = str(input("Are you travelling in the morning, afternoon or evening?: "))
        timeOfDay = timeOfDay.lower()
        if timeOfDay == 'morning' or 'evening':
                
            time = 1
                
        else:
                
            time = 0
        
        if trainDeparture == 'acle':
        
        routeInformation = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
                                     [0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],
                                     [0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],
                                     [0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],
                                     [1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],
                                     [1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],
                                     [1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],
                                     [1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        routeLate        = np.array([[0     , 0     , 0     , 1     , 0   , 
                                      0     , 1     , 0     , 1     , 1   ,
                                      1     , 1     , 1     , 0     , 0   ,
                                      1     , 0     , 0     , 1     , 0   ,
                                      0     , 0     , 0     , 0     , 0   ,
                                      0     , 0     , 1     , 1     , 0   ,
                                      0     , 1     , 0     , 0     , 1   ,
                                      1     , 0     , 1     , 0     , 0]]).T
    
        delayTimes = {5, 2, 7, 1, 7, 11, 2, 3, 1, 10, 8, 4, 6, 3, 2, 
                      6, 3, 9, 6, 1, 2, 8, 17, 5, 2, 4, 1, 7, 3, 6, 4,
                      8, 12, 6, 7, 2, 12, 3, 6, 1, 5, 8, 6, 14, 5, 6, 2}
        
    elif trainDeparture == 'attleborough':
            
        routeInformation = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],    
                                     [0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],
                                     [0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],
                                     [0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],
                                     [1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],
                                     [1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],
                                     [1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],
                                     [1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        routeLate        = np.array([[0     , 0     , 0     , 0     , 0   , 
                                      0     , 1     , 0     , 0     , 1   ,
                                      0     , 1     , 0     , 0     , 0   ,
                                      1     , 0     , 0     , 1     , 0   ,
                                      0     , 0     , 0     , 0     , 0   ,
                                      0     , 0     , 0     , 1     , 0   ,
                                      0     , 1     , 0     , 0     , 0   ,
                                      1     , 0     , 1     , 0     , 0]]).T
    
        delayTimes = {10, 2, 5, 8, 3, 12, 4, 5, 2, 2, 15, 35, 15, 3, 17, 31, 26,
                      4, 16, 4, 21, 4, 1, 4, 4, 6, 3, 7, 6, 4, 4, 7, 11, 5,
                      7, 2, 9, 4, 1, 1, 2, 1, 4, 2, 5}
    
    elif trainDeparture == 'beccles':
            
        routeInformation = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],    
                                     [0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],
                                     [0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],
                                     [0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],
                                     [1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],
                                     [1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],
                                     [1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],
                                     [1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        routeLate        = np.array([[0     , 0     , 0     , 0     , 0   , 
                                      0     , 0     , 0     , 0     , 0   ,
                                      0     , 1     , 0     , 0     , 0   ,
                                      1     , 0     , 0     , 0     , 0   ,
                                      0     , 0     , 0     , 0     , 0   ,
                                      0     , 0     , 0     , 0     , 0   ,
                                      0     , 0     , 0     , 1     , 0   ,
                                      1     , 0     , 0     , 0     , 0]]).T
    
        delayTimes = {1, 3, 3, 6, 2, 3, 4, 8, 1, 3, 6, 3, 9, 12, 3, 8, 10, 3, 1,
                      6, 8, 4, 8, 2, 6, 4, 7, 4, 2, 7, 5, 3, 9, 10, 3, 9,
                      4, 6, 13, 6, 5, 4, 8, 8, 5, 7, 4, 4, 2, 5, 6, 6, 2}
        
    elif trainDeparture == 'cambridge':
            
        routeInformation = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],    
                                     [0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],
                                     [0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],
                                     [0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],
                                     [1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],
                                     [1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],
                                     [1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],
                                     [1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        routeLate        = np.array([[0     , 1     , 1     , 0     , 0   , 
                                      1     , 1     , 1     , 0     , 0   ,
                                      0     , 1     , 1     , 1     , 0   ,
                                      1     , 1     , 1     , 0     , 1   ,
                                      0     , 1     , 0     , 0     , 1   ,
                                      1     , 0     , 0     , 1     , 0   ,
                                      0     , 1     , 0     , 0     , 0   ,
                                      0     , 0     , 0     , 1     , 1]]).T
    
        delayTimes = {12, 4, 6, 2, 5, 8, 7, 4, 6, 5, 3, 4, 4, 10, 5, 9,
                      2, 20, 8, 14, 6, 12, 10, 8, 5, 3, 6, 13, 8, 16, 5,
                      8, 4, 2, 10, 4, 16, 5, 8, 9, 6, 2, 6, 3, 6, 3, 8, 10}
    
    elif trainDeparture == 'diss':
            
        routeInformation = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],    
                                     [0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],
                                     [0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],
                                     [0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],
                                     [1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],
                                     [1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],
                                     [1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],
                                     [1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        routeLate        = np.array([[1     , 1     , 0     , 0     , 0   , 
                                      0     , 1     , 1     , 1     , 0   ,
                                      0     , 1     , 0     , 1     , 1   ,
                                      1     , 0     , 0     , 0     , 1   ,
                                      0     , 0     , 0     , 0     , 1   ,
                                      1     , 1     , 0     , 0     , 0   ,
                                      0     , 0     , 0     , 1     , 1   ,
                                      0     , 1     , 0     , 0     , 0]]).T
    
        delayTimes = {9, 4, 8, 7, 9, 1, 7, 8, 5, 9, 3, 2, 10, 4, 6, 4,
                      18, 22, 2, 13, 4, 8, 2, 9, 6, 7, 3, 5, 12, 6, 5, 4, 9,
                      4, 9, 9, 4, 4, 1, 4, 5, 7, 8, 4, 2, 3, 3, 6, 1, 3}
    
    elif trainDeparture == 'ipswich':
            
        routeInformation = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],    
                                     [0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],
                                     [0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],
                                     [0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],
                                     [1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],
                                     [1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],
                                     [1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],
                                     [1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        routeLate        = np.array([[0     , 1     , 0     , 0     , 0   , 
                                      0     , 1     , 1     , 0     , 0   ,
                                      0     , 1     , 0     , 1     , 0   ,
                                      0     , 0     , 1     , 0     , 1   ,
                                      0     , 0     , 0     , 0     , 0   ,
                                      0     , 1     , 0     , 0     , 0   ,
                                      0     , 0     , 0     , 1     , 0   ,
                                      0     , 1     , 0     , 1     , 0]]).T
    
        delayTimes = {4, 6, 2, 8, 5, 12, 8, 4, 6, 3, 10, 5, 5, 4, 8, 2, 7, 
                      4, 8, 1, 21, 8, 10, 4, 6, 9, 3, 10, 4, 8, 22, 13, 10, 
                      4, 9, 10, 6, 2, 7, 4, 9, 5, 5}
    
    elif trainDeparture == 'norwich':
            
        routeInformation = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],    
                                     [0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],
                                     [0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],
                                     [0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],
                                     [1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],
                                     [1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],
                                     [1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],
                                     [1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        routeLate        = np.array([[0     , 1     , 1     , 1     , 0   , 
                                      0     , 0     , 1     , 1     , 0   ,
                                      0     , 1     , 0     , 1     , 0   ,
                                      1     , 0     , 1     , 0     , 1   ,
                                      0     , 1     , 0     , 0     , 0   ,
                                      0     , 0     , 1     , 1     , 0   ,
                                      1     , 1     , 0     , 0     , 1   ,
                                      1     , 1     , 0     , 1     , 0]]).T
    
        delayTimes = {3, 8, 5, 17, 13, 5, 9, 5, 8, 10, 5, 2, 2, 3, 2, 6, 
                      4, 9, 10, 3, 2, 3, 8, 10, 3, 6, 8, 8, 6, 5, 7, 3, 12,
                      10, 5, 3, 2, 2, 8, 4, 7, 2, 9, 5, 14, 9, 3, 12, 10}
    
    elif trainDeparture == 'peterborough':
            
        routeInformation = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],    
                                     [0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],
                                     [0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],
                                     [0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],
                                     [1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],
                                     [1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],
                                     [1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],
                                     [1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        routeLate        = np.array([[0     , 1     , 1     , 1     , 0   , 
                                      0     , 0     , 1     , 1     , 0   ,
                                      1     , 1     , 0     , 1     , 0   ,
                                      1     , 1     , 1     , 0     , 1   ,
                                      0     , 1     , 0     , 0     , 1   ,
                                      0     , 0     , 0     , 1     , 0   ,
                                      0     , 1     , 0     , 0     , 1   ,
                                      1     , 0     , 1     , 1     , 0]]).T
    
        delayTimes = {6, 2, 9, 14, 10, 4, 8, 9, 4, 6, 1, 1, 7, 3, 2, 9, 5,
                      8, 14, 9, 10, 4, 6, 8, 3, 2, 6, 9, 13, 5, 2, 6, 4,
                      9, 5, 6, 4, 9, 2, 3, 9, 6, 4, 5, 1, 7, 4, 12, 6}
        
    trainPredictions.weightAdjustment(routeInformation, routeLate, 15000)
        
    prediction = trainPredictions.prediction(np.array([day, stops, time]))
    percentage = prediction * 100
    print("There is up to a " , percentage , "% chance that your train will be delayed")
    
    predictedDelay = trainPredictions.timeMean(delayTimes)
    print("Your predicted train delay is " , predictedDelay , " minutes, should one occur.")
        
    
    
   
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    