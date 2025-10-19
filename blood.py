import sys
import pygame
import random
import time
import math

bloodRed1 = pygame.Color(159, 0, 0)
bloodRed2 = pygame.Color(127, 0, 0)
bloodRed3 = pygame.Color(95, 0, 0)

class Blood:
    def __init__(self, x, y, size):
        self.x = x + 50
        self.y = y + 50
        self.size = 0.1
        self.max = size

class Bloodstain:
    def __init__(self, gridSize, scale):
        self.blood = []
        self.s = pygame.Surface((gridSize * scale, gridSize * scale))
        self.s.set_alpha(223)
        self.s.fill(pygame.Color(255, 255, 255))
        self.s.set_colorkey(pygame.Color(255, 255, 255))


    def add(self, x, y, minSize, maxSize, start, spread, minCount, maxCount):
        for i in range(random.randint(minCount, maxCount)):
            self.blood.append(Blood(x + random.randint(-spread, spread), y + random.randint(-spread, spread), random.randint(minSize, maxSize)))
            self.blood[-1].size = max(0.1, start)

    def draw(self, window, scale):
        self.s.fill(pygame.Color(255, 255, 255))
        for blood in self.blood:
            pygame.draw.circle(self.s, bloodRed1, (blood.x / 100 * scale, blood.y / 100 * scale), math.log(blood.size) / 3 * scale)
        for blood in self.blood:
            pygame.draw.circle(self.s, bloodRed2, (blood.x / 100 * scale, blood.y / 100 * scale), math.log(blood.size) / 3.5 * scale)
        for blood in self.blood:
            if blood.size > 2:
                pygame.draw.circle(self.s, bloodRed3, (blood.x / 100 * scale, blood.y / 100 * scale), math.log(blood.size) / 4.5 * scale)

        window.blit(self.s,(0, 0))
            
    def update(self):
        for blood in self.blood:
            if blood.size < blood.max:
                blood.size += 0.1

