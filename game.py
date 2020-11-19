import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import numpy as np
import math


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, index, angle=0.0, length=16, max_steering=90, max_acceleration=0.05, ):
        super().__init__()
        self.index = index
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
        self.distanceToSee = 150
        self.state = [0.0, 0.0, 0.0 ]

        self.image_car = pygame.image.load(carImagePath).convert_alpha()
        self.image = self.image_car
        self.image_clean = self.image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image_clean, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.anglesToSee = [-50, -25, 0, 25, 50]
        
        

        self.laserDistances = [(self.position.x, self.position.y), (self.position.x, self.position.y), (self.position.x, self.position.y), (self.position.x, self.position.y), (self.position.x, self.position.y)]

    def update(self, action):

        self.steering     = action[self.index][0]*self.max_steering
        self.acceleration = action[self.index][1]*self.max_acceleration
        self.braking      = action[self.index][2]*self.max_braking

        self.velocity += (self.acceleration - self.braking - self.free_deceleration , 0)
        self.velocity.x = max(0, min(self.velocity.x, self.max_velocity))
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle)
        self.angle += degrees(angular_velocity)
        
        

        self.image = pygame.transform.rotate(self.image_clean, self.angle)
    
    def draw(self, surface):
        
        for angleOffset in self.anglesToSee:
            for j in range(self.distanceToSee):
                loc = (int(self.position.x + j*math.cos((self.angle + angleOffset)*3.14/180)), int(self.position.y - j*math.sin((self.angle + angleOffset)*3.14/180)))
                pixel = trackImage.get_at(loc)
                surface.fill((255, 255, 255), (loc, (1, 1)))
                if pixel[3] != 187:
                    break
        x, y = self.position.x, self.position.y
        x -= int(self.image.get_rect().width/2  + self.length*(math.cos(self.angle*3.14/180)))
        y -= int(self.image.get_rect().height/2 - self.length*(math.sin(self.angle*3.14/180)))

        surface.blit(self.image, (x , y))
        


        

def initVars():
    global current_dir, trackPath, trackImage, carImagePath, screen
    width = 1000
    height = 750
    pygame.init()  
    screen = pygame.display.set_mode((width, height))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    trackPath = os.path.join(current_dir, "data/track.png")
    trackImage = pygame.image.load(trackPath).convert_alpha()
    carImagePath = os.path.join(current_dir, "data/car.png")
    

class Game:
    def __init__(self):
        self.exit = False
        self.numberOfCars = 5
        self.cars = pygame.sprite.Group()
        for i in range(self.numberOfCars):
            self.cars.add(Car(200,350, index = i))
        self.draw()


    def step(self, action, render = True):
       
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.cars.update(action)

        
        if render:
            self.draw()
        
        
    def draw(self):
        screen.fill((0, 0, 0))
        screen.blit(trackImage, Vector2(0, 0))
        for car in self.cars:
            car.draw(screen)
        pygame.display.flip()
        
 


if __name__ == '__main__':
    initVars()
    game = Game()
    action = [0.0, 0.0, 0.0]
    
    i = 0
    while i < 2500:
        i += 1 
        # action = np.zeros( (game.numberOfCars, 3))
        action = np.random.randn(game.numberOfCars, 3)
        action[:, 0] *= 2
        action[:, 0] -=0.5
        # action[:, 1] = 1.0
        # action = [1.0, 1.0, 0.5]
        game.step(action)
    pygame.quit()