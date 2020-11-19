import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import numpy as np
import math


class Car:
    def __init__(self, x, y, angle=30.0, length=4, max_steering=90, max_acceleration=0.05):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 1
        self.max_braking = max_acceleration
        self.free_deceleration = 0.001
        self.acceleration = 0.0
        self.steering = 0.0
        self.braking = 0.0

        self.laserIntersections = [(self.position.x, self.position.y), (self.position.x, self.position.y), (self.position.x, self.position.y), (self.position.x, self.position.y), (self.position.x, self.position.y)]

    def update(self):
        self.velocity += (self.acceleration - self.braking - self.free_deceleration , 0)
        self.velocity.x = max(0, min(self.velocity.x, self.max_velocity))
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle)
        self.angle += degrees(angular_velocity)

        

def initVars():
    global current_dir, trackPath, trackImage

    current_dir = os.path.dirname(os.path.abspath(__file__))
    trackPath = "data/track.png"
    trackImage = pygame.image.load(trackPath).convert_alpha()

class Game:
    def __init__(self):
        pygame.init()   
        width = 1000
        height = 750
        self.screen = pygame.display.set_mode((width, height))
        self.exit = False
        initVars()
        
        carImagePath = "data/car.png"        
        self.car_image = pygame.image.load(carImagePath).convert_alpha()
        
        
        self.numberOfCars = 3
        self.cars = []
        for i in range(self.numberOfCars):
            self.cars.append(Car(200,350))
        self.draw()

    def step(self, action, render = True):
       
        
        # while not self.exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        for i in range(self.numberOfCars):
            self.cars[i].steering     = action[i][0]*self.cars[i].max_steering
            self.cars[i].acceleration = action[i][1]*self.cars[i].max_acceleration
            self.cars[i].braking      = action[i][2]*self.cars[i].max_braking
            self.cars[i].update()
        
        if render:
            self.draw()
        
        # Drawing
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(trackImage, Vector2(0, 0))

        for i in range(self.numberOfCars):
            for angleOffset in [-40, -20, 0, 20, 40]:
                for j in range(100):
                    loc = (int(self.cars[i].position.x + j*math.cos((self.cars[i].angle + angleOffset)*3.14/180)), int(self.cars[i].position.y - j*math.sin((self.cars[i].angle + angleOffset)*3.14/180)))
                    pixel = trackImage.get_at(loc)
                    self.screen.fill((angleOffset*3 + 120, 255, 255), (loc, (1, 1)))
                    if pixel[3] != 187:
                        break
            rotated = pygame.transform.rotate(self.car_image, self.cars[i].angle)
            self.screen.blit(rotated, self.cars[i].position)# * self.ppu - (rect.width / 2, rect.height / 2))
        pygame.display.flip()
        
            # self.clock.tick(self.ticks)
 


if __name__ == '__main__':
    game = Game()
    action = [0.0, 0.0, 0.0]
    
    i = 0
    while i < 2500:
        i += 1 
        # action = np.zeros( (game.numberOfCars, 3))
        action = np.random.randn(game.numberOfCars, 3)
        # action[:, 0] *= 2
        # action[:, 0] -=0.5
        action[:, 1] = 1.0
        # action = [1.0, 1.0, 0.5]
        game.step(action)
    pygame.quit()