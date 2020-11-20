import torch
import os
import numpy as np


class Args():

    def __init__(self):
        #Environment properties        
        self.carImagePath = "data/car.png"
        self.trackPath = "data/track.png"
        self.startingPositionX = 118
        self.startingPositionY = 435
        self.cameraHeight = 300
        self.width = 1500
        self.height = 1500
        self.bgColor = (120, 120, 120)

        #Car properties
        self.anglesToSee = [-50, -25, 0, 25, 50]
        self.numberOfLasers = len(self.anglesToSee)
        self.maxSteering = 45
        self.maxAcceleration = 0.1
        self.maxVelocity = 0.5
        self.freeDeceleration = 0.
        
        # Settings
        self.numberOfCars = 20
        self.render = True


    def getParamsDict(self):
        ret = {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}
        print('\nHYPERPARAMETERS = ', ret)
        return ret

        

def configure():
    
    args = Args()
    
    return args