
import pygame
from pygame.math import Vector2
from config import Args
import math
import numpy as np

 
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, configs: Args, index,  trackImage,   ):
        super().__init__()
        self.index = index
        self.trackImage = trackImage
        self.position = Vector2(x, y)
        self.carTopPosition = Vector2(x, y)
        self.lastPosition = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)


        self.configs = configs
        self.angle = configs.angle
        self.length = 16
        self.maxAcceleration = configs.maxAcceleration
        self.maxSteering = configs.maxSteering
        self.maxVelocity = configs.maxVelocity
        self.maxBraking = configs.maxBraking
        self.freeDeceleration = configs.freeDeceleration


        self.acceleration = 0.0
        self.steering = 0.0
        self.braking = 0.0
        self.distanceToSee = configs.distanceToSee
        self.color = np.array([255,255, 255])
        self.color[self.index % 3] = int(self.index*200/(configs.numberOfCars + 1))

        
        self.distance = 0
        self.reward = 0

        self.image_car = pygame.image.load(self.configs.carImagePath)
        self.image = self.image_car
        self.image_clean = self.image
        self.image = pygame.transform.rotate(self.image_clean, self.angle)

        self.dead = False

        self.laserDistances = [0.0 for i in range(self.configs.numberOfLasers)]
        self.pointsToMark = set()
        self.genTrackPoint = (self.carTopPosition.x, self.carTopPosition.y)
        self.trackPoints = set()
        

    def getPixelAt(self, dist, angleOffset):
        loc = [0,0]
        loc[0] = min(self.configs.width-1, max(0, int(self.carTopPosition.x + dist*math.cos((self.angle + angleOffset)*math.pi/180))))
        loc[1] = min(self.configs.height-1, max(0, int(self.carTopPosition.y - dist*math.sin((self.angle + angleOffset)*math.pi/180))))
        return self.trackImage.get_at(loc)



    def update(self, action):
        if not self.dead:
            ######### Car physics
            
            self.acceleration = action[1]*self.maxAcceleration
            self.braking      = action[2]*self.maxBraking

            self.velocity += (self.acceleration - self.braking - self.freeDeceleration , 0)
            self.velocity.x = max(0, min(self.velocity.x, self.maxVelocity))

            self.steering = action[0]*((self.maxSteering - 5)*(1 - (self.velocity.x/self.maxVelocity)) + 5) ##max steering angle should change with speed

            if self.steering:
                turning_radius = self.length / math.sin(math.radians(self.steering))
                angular_velocity = self.velocity.x / turning_radius
            else:
                angular_velocity = 0

            self.position += self.velocity.rotate(-self.angle)
            self.angle += math.degrees(angular_velocity)

            self.image = pygame.transform.rotate(self.image_clean, self.angle)

            self.carTopPosition = Vector2(self.position.x, self.position.y)
            self.carTopPosition.x += int(self.image.get_rect().width/2  + self.length*(math.cos(self.angle*math.pi/180)))
            self.carTopPosition.y += int(self.image.get_rect().height/2 - self.length*(math.sin(self.angle*math.pi/180)))
            
            ######## END CAR PHYSICS######
            
            self.pointsToMark = set()
            self.trackPoints = set()

            # Distance sensor
            for i in range(len(self.configs.anglesToSee)):
                angleOffset = self.configs.anglesToSee[i]
                pixel = None
                low = 0
                high = self.distanceToSee

                while low <= high:
                    midJ = (low + high)//2
                    pixel = self.getPixelAt(midJ, angleOffset)
                    if pixel[2] == 255: #Alpha 0 => Track
                        low = midJ + 1
                    else:
                        high = midJ - 1
                    if abs(low - high) <= 2:
                        loc = (int(self.carTopPosition.x + low*math.cos((self.angle + angleOffset)*3.14/180)), int(self.carTopPosition.y - low*math.sin((self.angle + angleOffset)*3.14/180)))
                        dist = np.linalg.norm(np.array(loc) - np.array(self.carTopPosition))
                        self.laserDistances[i] = dist
                        self.pointsToMark.add(loc)
                        if dist < 120:
                            self.trackPoints.add(loc)
                        break
                
                if pixel[2] == 255: #Alpha 0 => Track
                    self.laserDistances[i] = self.distanceToSee
            
            

            self.reward -= 0.05 # Time penalty

            # Reward for covering more distance
            if (np.linalg.norm(self.lastPosition - self.position)) > 20:
                self.reward += 3
                self.distance += 20
                self.lastPosition = (self.position.x, self.position.y)

            if self.reward < -5: # Time death
                self.dead = True
                self.reward -= 10

            for dist in self.laserDistances:
                if dist < 5: # Green death
                    self.dead = True
                    self.reward -= 10
            

            if self.configs.test: # For marking the track points
                self.genTrackPoint = (self.carTopPosition.x, self.carTopPosition.y)

        return self.laserDistances, self.dead, self.reward, self.distance
    
    def draw(self, surface, cameraPosition):
        surface.blit(self.image, self.position - cameraPosition)
        if not self.dead:
            for point in self.pointsToMark:
                surface.fill((255, 255, 255), (point - cameraPosition, (3, 3)))

