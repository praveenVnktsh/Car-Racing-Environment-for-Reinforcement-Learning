import torch
import os
import numpy as np


class Args():

    def __init__(self):
        self.numberOfLasers = 5
        self.numberOfCars = 100
        self.carImagePath = "data/car.png"
        self.trackPath = "data/track.png"
        self.width = 1000
        self.height = 750


    def getParamsDict(self):
        ret = {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}
        print('\nHYPERPARAMETERS = ', ret)
        return ret

        

def configure():
    
    args = Args()
    
    return args