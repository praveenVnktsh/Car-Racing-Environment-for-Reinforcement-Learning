from car import Car
import pygame
from pygame.math import Vector2
import numpy as np
from config import Args, configure
import time


class Environment:
    def __init__(self, config:Args, trackImage):
        self.exit = False
        
        self.cars = pygame.sprite.Group()
        self.config = config

        for i in range(self.config.numberOfCars):
            
            self.cars.add(Car(200,350, index = i, configs = self.config, trackImage=  trackImage))
        self.draw()

    def step(self, action, render = True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        state = np.zeros((self.config.numberOfCars, self.config.numberOfLasers))
        rewards = np.zeros((self.config.numberOfCars,))
        dead = np.zeros((self.config.numberOfCars,))
        i = 0
        for car in self.cars:
            state[i], dead[i], rewards[i] = car.update(action, screen)
            
            i += 1

        if render:
            self.draw()
        
        return state, dead, rewards
        
        
        
    def draw(self):
        screen.fill((0, 0, 0))
        screen.blit(trackImage, Vector2(0, 0))
        for car in self.cars:
            car.draw(screen)
        pygame.display.flip()
         
 


if __name__ == '__main__':
    
    pygame.init()  
    configs = configure()
    screen = pygame.display.set_mode((configs.width, configs.height))
    trackImage = pygame.image.load(configs.trackPath).convert_alpha()
    
    
    game = Environment(configs, trackImage)
    action = [0.0, 0.0, 0.0]
    
    i = 0
    startTime = time.time()
    while i < 2500:
        i += 1 
        action = np.random.randn(configs.numberOfCars, 3)
        action[:, 0] *= 2
        action[:, 0] -=0.5
        # action = np.zeros((game.numberOfCars, 3))
        # action[:, 1] = 1.0
        game.step(action, render = True)
    endTime = time.time()

    print('Took ', endTime - startTime, 'to finish Simulation')
    pygame.quit()