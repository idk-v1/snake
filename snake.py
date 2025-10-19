import sys
import pygame
import random
import time
import math

from mouse import *
from blood import *
from utils import *

snakeBlue = pygame.Color(63, 63, 255)
snakeYellow = pygame.Color(255, 255, 63)
snakeBlue2 = pygame.Color(47, 47, 255)
snakeYellow2 = pygame.Color(223, 223, 31)

tongueRed = pygame.Color(255, 0, 0)

eyeWhite = pygame.Color(255, 255, 255)
eyeMain = pygame.Color(0, 0, 0)

bloodRed1 = pygame.Color(159, 0, 0)

class Segment:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.canMove = False
        self.bit = 0

class Snake:
    def __init__(self, x, y, length):
        self.nextDir = 0
        self.segs = []
        for i in range(length):
            posX = x * 100 - math.cos(toRad(self.nextDir)) * i * 100
            posY = y * 100 - math.sin(toRad(self.nextDir)) * i * 100
            self.segs.append(Segment(posX, posY, self.nextDir))
            self.segs[-1].canMove = True
        self.shouldAdd = False
        self.speed = 10
        self.rad = 0.8
        self.dead = 0
        self.tongueCycle = 0


    def draw(self, window):
        for i in range(len(self.segs) - 1, 0, -1):

            if self.segs[i].bit == 3:
                continue
                
            x = self.segs[i].x / 100 + 0.5
            y = self.segs[i].y / 100 + 0.5
            x1 = self.segs[i - 1].x / 100 + 0.5
            y1 = self.segs[i - 1].y / 100 + 0.5

            rad = self.rad / 2
            if len(self.segs) - 1 - i < 5:
                rad = (self.rad - 0.05 * (5 - (len(self.segs) - 1 - i))) / 2

            color = snakeBlue
            if i // 4 % 2:
                color = snakeYellow

            drawCircle(window, color, x, y, rad)
            if self.segs[i - 1].bit == 3:
                continue

            # added little bit to get rid of bump from circle
            nudge = -0.01
            #if going around corner, use more resolution
            if self.segs[i].x != self.segs[i - 1].x and self.segs[i].y != self.segs[i - 1].y:
                avgx1 = (x + x1) / 2
                avgy1 = (y + y1) / 2
                avgx2 = (x + avgx1) / 2
                avgy2 = (y + avgy1) / 2
                avgx3 = (x1 + avgx1) / 2
                avgy3 = (y1 + avgy1) / 2

                drawCircle(window, color, avgx1, avgy1, rad)
                drawCircle(window, color, avgx2, avgy2, rad)
                drawCircle(window, color, avgx3, avgy3, rad)

                drawLinePt(window, color, x + nudge, y + nudge, avgx2 + nudge, avgy2 + nudge, rad * 2)
                drawLinePt(window, color, avgx2 + nudge, avgy2 + nudge, avgx1 + nudge, avgy1 + nudge, rad * 2)
                drawLinePt(window, color, avgx1 + nudge, avgy1 + nudge, avgx3 + nudge, avgy3 + nudge, rad * 2)
                drawLinePt(window, color, avgx3 + nudge, avgy3 + nudge, x1 + nudge, y1 + nudge, rad * 2)

            else:
                drawLinePt(window, color, x + nudge, y + nudge, x1 + nudge, y1 + nudge, rad * 2)

        # head
        rad = self.rad / 2
        if len(self.segs) - 1 < 5:
            rad = (self.rad - 0.05 * (5 - (len(self.segs) - 1))) / 2
                
        x = self.segs[0].x / 100 + 0.5
        y = self.segs[0].y / 100 + 0.5

        # tongue
        tongue = rotPoint(x, y, max(math.sin(toRad(self.tongueCycle)), 0.0) / 2, self.segs[0].dir)
        drawLinePt(window, tongueRed, x, y, tongue[0], tongue[1], 1 / 10)
        drawLineRot(window, tongueRed, tongue[0], tongue[1], 1 / 6, self.segs[0].dir + 45, 1 / 15)
        drawLineRot(window, tongueRed, tongue[0], tongue[1], 1 / 6, self.segs[0].dir - 45, 1 / 15)

        # head
        drawCircle(window, snakeBlue2, x, y, rad)

        # eyes
        rad = self.rad / 2
        eye = rotPoint(x, y, 1 / 6, self.segs[0].dir + 45)
        drawCircle(window, eyeWhite, eye[0], eye[1], rad / 4)
        if self.dead:
            drawLineRot(window, eyeMain, eye[0], eye[1], rad / 5, self.segs[0].dir + 45, 0.05)
            drawLineRot(window, eyeMain, eye[0], eye[1], rad / 5, self.segs[0].dir + 135, 0.05)
            drawLineRot(window, eyeMain, eye[0], eye[1], rad / 5, self.segs[0].dir + 225, 0.05)
            drawLineRot(window, eyeMain, eye[0], eye[1], rad / 5, self.segs[0].dir + 315, 0.05)
        else:
            drawCircle(window, eyeMain, eye[0], eye[1], rad / 4.5)

        eye = rotPoint(x, y, 1 / 6, self.segs[0].dir - 45)
        drawCircle(window, eyeWhite, eye[0], eye[1], rad / 4)
        if self.dead:
            drawLineRot(window, eyeMain, eye[0], eye[1], rad / 5, self.segs[0].dir + 45, 0.05)
            drawLineRot(window, eyeMain, eye[0], eye[1], rad / 5, self.segs[0].dir + 135, 0.05)
            drawLineRot(window, eyeMain, eye[0], eye[1], rad / 5, self.segs[0].dir + 225, 0.05)
            drawLineRot(window, eyeMain, eye[0], eye[1], rad / 5, self.segs[0].dir + 315, 0.05)
        else:
            drawCircle(window, eyeMain, eye[0], eye[1], rad / 4.5)        
        

    def length(self):
        return len(self.segs)

    def isInSquare(self, x, y):
        for seg in self.segs:
            if math.ceil(seg.x / 100) == x and math.ceil(seg.y / 100) == y:
                return True
            if math.floor(seg.x / 100) == x and math.floor(seg.y / 100) == y:
                return True
        return False

    def changeDir(self, dir):
        if self.segs[0].dir % 180 != dir % 180:
            self.nextDir = dir

    # returns 1 if ate apple, -1 if ate tail, 0 other
    def update(self, mouse, gridSize, bloodstain):
        ret = 0

        if self.dead:
            return -1

        self.tongueCycle += 5
        
        for seg in self.segs:
            if seg.canMove:
                seg.x += int(math.cos(toRad(seg.dir))) * self.speed
                seg.y += int(math.sin(toRad(seg.dir))) * self.speed
        
        # aligned to grid
        if self.segs[0].x % 100 == 0:
            if self.segs[0].y % 100 == 0:

                # eat apple
                if math.sqrt(math.pow(self.segs[0].x - mouse.x, 2) + math.pow(self.segs[0].y - mouse.y, 2)) / 100 < (self.rad + mouse.rad) / 2:
                    self.shouldAdd = True
                    ret = 1

                # new segment can start moving
                self.segs[-1].canMove = True
                
                if self.shouldAdd: # add if needed
                    dir = self.segs[-1].dir
                    x = self.segs[-1].x
                    y = self.segs[-1].y
                    self.segs.append(Segment(x, y, dir))
                    self.shouldAdd = False

                # update segments to last segment direction
                for i in (range(len(self.segs) - 1, 0, -1)):
                    self.segs[i].dir = self.segs[i - 1].dir

                self.segs[0].dir = self.nextDir

                # spread bite
                for i in (range(len(self.segs) - 1, 0, -1)):
                    if self.segs[i].bit:
                        if self.segs[i].bit < 3:
                            self.segs[i].bit += 1
                        elif self.segs[i - 1].bit == 0:
                            self.segs[i - 1].bit = 1
                        bloodstain.add(self.segs[i - 1].x, self.segs[i - 1].y, 3, 10, 3, 50, 4, 6)

                # collide with tail
                bit = False
                for i in range(1, len(self.segs)):
                    if bit or self.segs[i].bit == 3:
                        bit = True
                        self.segs[i].canMove = False
                    else:
                        if self.segs[0].x == self.segs[i].x:
                            if self.segs[0].y == self.segs[i].y:
                                if self.segs[i].canMove:
                                    self.segs[i].bit = 3
                                    bit = True
                                    bloodstain.add(self.segs[i].x, self.segs[i].y, 3, 10, 3, 50, 4, 6)
                              
        # collide with wall
        if math.ceil(self.segs[0].x / 100 + self.rad) > gridSize:
            ret = -1
        if math.ceil(self.segs[0].y / 100 + self.rad) > gridSize:
            ret = -1
        if math.floor(self.segs[0].x / 100 - self.rad) < -1:
            ret = -1
        if math.floor(self.segs[0].y / 100 - self.rad) < -1:
            ret = -1
        if ret == -1:
            self.dead = -1
            bloodstain.add(self.segs[0].x, self.segs[0].y, 5, 6, 1, 25, 2, 4)

        if self.segs[0].bit:
            self.dead = 1
            ret = -1
        
        return ret
