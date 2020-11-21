from car import Car
import pygame
from pygame.math import Vector2
import numpy as np
from config import Args, configure
import time

class Environment:
    def __init__(self, config:Args, trackImage):
        self.exit = False
        self.index = 0
        self.clock = pygame.time.Clock()
        
        self.cars = pygame.sprite.Group()
        self.cameraPosition = Vector2(configs.startingPositionX - configs.cameraHeight//2,configs.startingPositionY - configs.cameraHeight//2)
        self.cameraPositions = []
        self.cameraPositions.append((self.cameraPosition.x, self.cameraPosition.y))
        
        self.config = config

        for i in range(self.config.numberOfCars):
            self.cars.add(Car(configs.startingPositionX , configs.startingPositionY, index = i, configs = self.config, trackImage=  trackImage))
        
        self.draw()

    def step(self, action, render = True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        state = np.zeros((self.config.numberOfCars, self.config.numberOfLasers))
        rewards = np.zeros((self.config.numberOfCars,))
        dead = np.zeros((self.config.numberOfCars,))
        self.index += 1

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            action[:, 1] = 1.0
        if pressed[pygame.K_LEFT]:
            action[:, 0] = 1.0
        if pressed[pygame.K_RIGHT]:
            action[:, 0] = -1.0
        if pressed[pygame.K_SPACE]:
            action[:, 2] = 1.0

        
        bestCarDistance =  0
        i = 0
        for car in self.cars:
            state[i], dead[i], rewards[i], carDistance = car.update(action, screen)
            if carDistance > bestCarDistance:
                bestCarDistance = carDistance
                self.cameraPosition.x = car.position.x - self.config.cameraHeight//2
                self.cameraPosition.y = car.position.y - self.config.cameraHeight//2
                if car.angle > 0:
                    self.cameraPosition.y -= self.config.cameraOffset
                elif car.angle < 0:
                    self.cameraPosition.y += self.config.cameraOffset
                    # self.cameraPosition.x += self.config.cameraOffset
            i += 1
        
        if len(self.cameraPositions) > 10:
            self.cameraPositions.pop(0)
        self.cameraPositions.append((self.cameraPosition.x, self.cameraPosition.y))
        mean = np.mean(self.cameraPositions, 0)
        self.cameraPosition =Vector2(int(mean[0]), int(mean[1]))

        if render:
            self.draw()
            self.clock.tick(60)
        return state, dead, rewards, self.index
        
    def reset(self):
        self.index = 0
        self.cars = pygame.sprite.Group()
        self.cameraPosition = Vector2(configs.startingPositionX - configs.cameraHeight//2,configs.startingPositionY - configs.cameraHeight//2)
        self.cameraPositions = []
        self.cameraPositions.append((self.cameraPosition.x, self.cameraPosition.y))

        for i in range(self.config.numberOfCars):
            self.cars.add(Car(configs.startingPositionX , configs.startingPositionY, index = i, configs = self.config, trackImage=  trackImage))
        
        self.draw()

    
    def draw(self):
        screen.fill(configs.bgColor)
        cropRect = (self.cameraPosition.x, self.cameraPosition.y, self.config.cameraHeight, self.config.cameraHeight)
        screen.blit(trackImage,(0,0),cropRect)
        for car in self.cars:
            car.draw(screen, self.cameraPosition)
        pygame.display.flip()
         
 


if __name__ == '__main__':
    
    pygame.init()  
    configs = configure()
    screen = pygame.display.set_mode((configs.cameraHeight, configs.cameraHeight))
    trackImage = pygame.image.load(configs.trackPath).convert_alpha()
    

    env = Environment(configs, trackImage)
    while True:
        action = np.zeros((configs.numberOfCars, 3))
        
        state, dead, rewards, index = env.step(action, render = configs.render)
        print(index)
        if 0.0 not in dead:
            time.sleep(2)
            env.reset()

    