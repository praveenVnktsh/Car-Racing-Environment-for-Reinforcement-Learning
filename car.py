
import pygame
from pygame.math import Vector2
from config import Args
import math
import numpy as np

 
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, configs: Args, index,  trackImage, angle=0.0, length=16, max_steering=90, max_acceleration=0.1,  ):
        super().__init__()
        self.index = index
        self.trackImage = trackImage
        self.position = Vector2(x, y)
        self.lastPosition = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 1.5
        self.max_braking = max_acceleration
        self.free_deceleration = 0.001
        self.acceleration = 0.0
        self.configs = configs
        self.steering = 0.0
        self.braking = 0.0
        self.distanceToSee = 75
        self.state = [0.0, 0.0, 0.0 ]

        self.ticks = 0
        self.reward = 0

        self.image_car = pygame.image.load(self.configs.carImagePath).convert_alpha()
        self.image = self.image_car
        self.image_clean = self.image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image_clean, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.anglesToSee = [-50, -25, 0, 25, 50]

        self.dead = False
        
        

        self.laserDistances = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.pointsToMark = []

    def getPixelAt(self, dist, angleOffset):
        loc = (int(self.position.x + dist*math.cos((self.angle + angleOffset)*3.14/180)), int(self.position.y - dist*math.sin((self.angle + angleOffset)*3.14/180)))
        return self.trackImage.get_at(loc)



    def update(self, action, surface):
        if not self.dead:
            self.steering     = action[self.index][0]*self.max_steering
            self.acceleration = action[self.index][1]*self.max_acceleration
            self.braking      = action[self.index][2]*self.max_braking

            self.velocity += (self.acceleration - self.braking - self.free_deceleration , 0)
            self.velocity.x = max(0, min(self.velocity.x, self.max_velocity))
            if self.steering:
                turning_radius = self.length / math.sin(math.radians(self.steering))
                angular_velocity = self.velocity.x / turning_radius
            else:
                angular_velocity = 0

            self.position += self.velocity.rotate(-self.angle)
            self.angle += math.degrees(angular_velocity)
            self.image = pygame.transform.rotate(self.image_clean, self.angle)
            self.pointsToMark = []
            for i in range(len(self.anglesToSee)):
                angleOffset = self.anglesToSee[i]
                pixel = None

                low = 0
                high = self.distanceToSee
                while low <= high:
                    midJ = (low + high)//2
                    pixel = self.getPixelAt(midJ, angleOffset)
                    # 
                    if pixel[3] == 187:
                        low = midJ + 1
                    else:
                        high = midJ - 1
                        
                    if abs(low - high) <= 2:
                        loc = (int(self.position.x + low*math.cos((self.angle + angleOffset)*3.14/180)), int(self.position.y - low*math.sin((self.angle + angleOffset)*3.14/180)))
                        dist = np.linalg.norm(np.array(loc) - np.array(self.position))
                        self.laserDistances[i] = dist
                        # self.pointsToMark.append(self.position)
                        self.pointsToMark.append(loc)
                        break

                if pixel[3] == 187:
                    self.laserDistances[i] = self.distanceToSee

            # if sum(self.laserDistances) < 50:
            #     self.dead = True
            #     self.reward -= 10
            for dist in self.laserDistances:
                if dist < 1:
                    self.dead = True
                    self.reward -= 10



            self.reward -= 0.1
            if (np.linalg.norm(np.array(self.lastPosition) - np.array(self.position))) > 20:
                self.reward += 3
                self.lastPosition = (self.position.x, self.position.y)

        return self.laserDistances, self.dead, self.reward
    
    def draw(self, surface):
        x, y = self.position.x, self.position.y
        x -= int(self.image.get_rect().width/2  + self.length*(math.cos(self.angle*3.14/180)))
        y -= int(self.image.get_rect().height/2 - self.length*(math.sin(self.angle*3.14/180)))
        surface.blit(self.image, (x , y))
        # if self.pointsToMark != []:
        #     pygame.draw.lines(surface, (255, 255, 255), False, self.pointsToMark)
        if not self.dead:
            for point in self.pointsToMark:
                surface.fill((255, 255, 255), (point, (3, 3)))

