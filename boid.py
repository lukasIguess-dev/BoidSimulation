import pygame
import time
import random
from pygame.math import*
class Boid:
    def __init__(self) -> None:
        self.__rect = pygame.Rect(random.randrange(100,900),random.randrange(100,600),4,4)
        self.__speed = 0.1
        self.__velocity = Vector2(0,0)
        self.__nextMove = time.time()
        self.__moveDelay = 0
        self.__randomise_factor = 0.4 # the lower the more chaotic
        self.__colors = [(255,255,255), (255,0,0)]
        self.__min_speed = 3
        self.__max_speed = 5

        self.__protected_range = 3
        self.__visible_range = 40
        self.__avoidfactor = 0.05
        self.__matchingfactor = 0.6 #0.4

    def get_pos(self) -> Vector2:
        return Vector2(self.__rect.x, self.__rect.y)
    def get_velocity(self) -> Vector2:
        return Vector2(self.__velocity.x, self.__velocity.y)
    
    def __calc_distance(self, v1:Vector2, v2:Vector2) -> float:
        distance = v1.distance_to(v2)
        return distance
        
    
    # evaluate new move direction by logic
    def think(self, boidList):
        
        if self.__nextMove < time.time():
            
            self.__nextMove = time.time() + self.__moveDelay + random.randrange(-1,1) # reset next time to change direction
            self.__velocity = Vector2(lerp(random.random()*2-1, self.__velocity.x, self.__randomise_factor), lerp(random.random()*2-1, self.__velocity.y,self.__randomise_factor)).normalize()
            
        # 0 all temporary parameters
        vel_avg = Vector2(0,0)
        close_d = Vector2(0,0)
        neighbouring_boids = 0

        for boid in boidList:
            if boid != self:
                dist = self.__calc_distance(self.get_pos(),boid.get_pos())
                
                # seperation
                if dist <= self.__protected_range:
                    self.__color = self.__colors[1] # recolor self

                    close_d = Vector2(self.get_pos().x-boid.get_pos().x, self.get_pos().y-boid.get_pos().y)

                    self.__velocity += close_d * self.__avoidfactor
                    if self.__velocity != Vector2(0,0):
                        self.__velocity.normalize()
                else:
                    self.__color = self.__colors[0]

                # alignment
                if dist < self.__visible_range:
                    vel_avg += boid.get_velocity()
                    neighbouring_boids += 1
        
        # alignment
        if neighbouring_boids > 0:
            vel_avg =  vel_avg / neighbouring_boids
            self.__velocity += (vel_avg - self.__velocity)* self.__matchingfactor

        # apply min/max speed
        speed = self.__velocity.length()
        if speed < self.__min_speed:
            self.__velocity = (self.__velocity/speed)*self.__min_speed
        if speed > self.__max_speed:    
            self.__velocity = (self.__velocity/speed)*self.__max_speed



    def move(self, dt):
        self.__rect.x += self.__velocity.x * self.__speed * dt
        self.__rect.y += self.__velocity.y * self.__speed * dt

    # update boid
    def update(self, dt, boidList):
        self.think(boidList)
        self.move(dt)
        # check if boid went out of bounds
        screen_width = 1000
        screen_height = 700
        if self.__rect.x > screen_width-10: self.__rect.x = 10
        elif self.__rect.x < 10: self.__rect.x = screen_width-10

        if self.__rect.y > screen_height-10: self.__rect.y = 10
        elif self.__rect.y < 10: self.__rect.y = screen_height-10
    
    # draw boid to canvas
    def draw(self, surface:pygame.Surface) -> None:
        pygame.draw.rect(surface, self.__colors[0], self.__rect)
    
