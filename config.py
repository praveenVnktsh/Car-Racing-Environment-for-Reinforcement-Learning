import torch
import os
import numpy as np


class Args():

    def __init__(self):
        self.numberOfLasers = 5
        self.numberOfCars = 20
        self.carImagePath = "data/car.png"
        self.trackPath = "data/track.png"
        self.startingPositionX = 118
        self.startingPositionY = 435
        self.cameraHeight = 300
        self.width = 1500
        self.height = 1500


    def getParamsDict(self):
        ret = {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}
        print('\nHYPERPARAMETERS = ', ret)
        return ret

        

def configure():
    
    args = Args()
    
    return args