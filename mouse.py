import sys
import pygame
import random
import time
import math

from snake import *
from utils import *

mouseFur = pygame.Color(127, 127, 127)
mouseEar = pygame.Color(95, 95, 95)
mousePink = pygame.Color(255, 191, 191)

eyeWhite = pygame.Color(255, 255, 255)
eyeMain = pygame.Color(0, 0, 0)

dirt = pygame.Color(59, 31, 0)

class Mouse:
    def __init__(self, x, y):
        self.x = x * 100
        self.y = y * 100
        self.rad = 0.75
        self.dir = random.randrange(0, 360, 5)
        self.speed = 10
        self.hole = 45
        self.searchDir = 0
        self.rotQueue = 0

    def draw(self, window):

        x = self.x / 100 + 0.5
        y = self.y / 100 + 0.5

        if self.hole < 180:
            drawCircle(window, dirt, x, y, math.sin(toRad(self.hole)) / 2)
        if self.hole < 90:
            return
    
        # tail
        drawLineRot(window, mousePink, x, y, -1, self.dir, 0.1)

        # body
        drawCircle(window, mouseFur, x, y, self.rad / 2)

        # nose
        nose = rotPoint(x, y, self.rad / 3, self.dir)
        drawCircle(window, mouseFur, nose[0], nose[1], 1 / 5)
        nose = rotPoint(x, y, self.rad / 1.5, self.dir)
        drawCircle(window, mousePink, nose[0], nose[1], 1 / 15)

        #ears
        earAngle = 75
        ears = rotPoint(x, y, self.rad / 2, self.dir + earAngle)
        drawCircle(window, mouseEar, ears[0], ears[1], 1 / 10)
        ears = rotPoint(x, y, self.rad / 2, self.dir - earAngle)
        drawCircle(window, mouseEar, ears[0], ears[1], 1 / 10)

        #eyes
        eyeAngle = 35
        eyes = rotPoint(x, y, self.rad / 2, self.dir + eyeAngle)
        drawCircle(window, eyeWhite, eyes[0], eyes[1], 1 / 10)
        drawCircle(window, eyeMain, eyes[0], eyes[1], 1 / 11)
        eyes = rotPoint(x, y, self.rad / 2, self.dir - eyeAngle)
        drawCircle(window, eyeWhite, eyes[0], eyes[1], 1 / 10)
        drawCircle(window, eyeMain, eyes[0], eyes[1], 1 / 11)


    def update(self, snake, gridSize):
        if self.hole < 135:
            self.hole += 2
            return
        
        self.x += math.cos(toRad(self.dir)) * self.speed
        self.y += math.sin(toRad(self.dir)) * self.speed
        if self.rotQueue == 0:
            self.rotQueue = random.randint(-15, 15)
        if self.rotQueue < 0:
            self.dir -= 2
            self.rotQueue += 1
        else:
            self.dir += 2
            self.rotQueue -= 1

        shouldChange = False
        if math.ceil(self.x / 100 + self.rad + 0.1) > gridSize:
            shouldChange = True
        if math.ceil(self.y / 100 + self.rad + 0.1) > gridSize:
            shouldChange = True
        if math.floor(self.x / 100 - self.rad - 0.1) < -1:
            shouldChange = True
        if math.floor(self.y / 100 - self.rad - 0.1) < -1:
            shouldChange = True

        if snake.isInSquare(math.ceil(self.x / 100 - self.rad - 0.1), math.ceil(self.y / 100 - self.rad - 0.1)):
            shouldChange = True
        if snake.isInSquare(math.floor(self.x / 100 + self.rad + 0.1), math.ceil(self.y / 100 - self.rad - 0.1)):
            shouldChange = True
        if snake.isInSquare(math.ceil(self.x / 100 - self.rad - 0.1), math.floor(self.y / 100 + self.rad + 0.1)):
            shouldChange = True
        if snake.isInSquare(math.floor(self.x / 100 + self.rad + 0.1), math.floor(self.y / 100 + self.rad + 0.1)):
            shouldChange = True


        if shouldChange:
            self.x -= math.cos(toRad(self.dir)) * self.speed
            self.y -= math.sin(toRad(self.dir)) * self.speed
            if self.searchDir == 0:
                self.searchDir = random.choice((-1, 1))
            else:
                self.dir += self.searchDir * 30
        else:
            self.searchDir = 0

                    
