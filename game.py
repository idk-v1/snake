# BUGS:
# - Blood from bitten snake only spawns on head and tail


import sys
import pygame
import random
import time
import math

from snake import *
from mouse import *
from blood import *
from utils import *


gridSize = 10
scoreBoxH = 1 / 2

gameGrass1 = pygame.Color(63, 191, 63)
gameGrass2 = pygame.Color(31, 159, 31)

menuGrass1 = pygame.Color(31, 159, 31)
menuGrass2 = pygame.Color(0, 95, 0)

scoreBarColor = pygame.Color(15, 63, 15)
scoreBarMenuColor = pygame.Color(0, 31, 0)

textColor = pygame.Color(255, 255, 255)

# major game change (eg. classic snake to snake with mice)
# minor game change (eg. adding mice appearing from holes)
# unnoticable/bugfix (eg. cleaning up)
version = "2.8.2"


pygame.init()
font = pygame.font.SysFont(None, scale)
smallFont = pygame.font.SysFont(None, scale // 2)

window = pygame.display.set_mode((gridSize * scale, (gridSize + scoreBoxH) * scale))
pygame.display.set_caption("Snake")

initSnakeLen = 3
snake = Snake(gridSize / 2, gridSize / 2, initSnakeLen)

mouse = Mouse(int(gridSize / 4), int(gridSize / 4))

bloodstain = Bloodstain(gridSize, scale)

dt = 0
last = time.time() * 1000

key = 0

inGame = False
hasPlayed = False

ticksPerSec = 30

while True:

    window.fill(pygame.Color(0, 0, 0))

    if not inGame:
        # draw grass tiles
        for x in range(gridSize):
            for y in range(gridSize):
                if (x + y) % 2:
                    drawRect(window, menuGrass1, x, y, 1, 1, -1, -1)
                else:
                    drawRect(window, menuGrass2, x, y, 1, 1, -1, -1)
    else:
        # draw grass tiles
        for x in range(gridSize):
            for y in range(gridSize):
                if (x + y) % 2:
                    drawRect(window, gameGrass1, x, y, 1, 1, -1, -1)
                else:
                    drawRect(window, gameGrass2, x, y, 1, 1, -1, -1)

    if inGame or hasPlayed:
        now = time.time() * 1000
        dt += now - last
        while dt >= 1000 / ticksPerSec:
            dt -= 1000 / ticksPerSec

            bloodstain.update()
            
            mouse.update(snake, gridSize)
            
            ret = snake.update(mouse, gridSize, bloodstain)
            if ret == 1: # snake ate mouse
                bloodstain.add(mouse.x, mouse.y, 2, 4, 0, 50, 3, 6)

                newMouseX = random.randrange(0, gridSize)
                newMouseY = random.randrange(0, gridSize)
                while snake.isInSquare(newMouseX, newMouseY):
                    newMouseX = random.randrange(0, gridSize)
                    newMouseY = random.randrange(0, gridSize)
                mouse = Mouse(newMouseX, newMouseY)

            elif ret == -1: # snake dead
                inGame = False
                
        last = now

        bloodstain.draw(window, scale)
        
        mouse.draw(window)

        snake.draw(window)
        
        # draw score area
        if inGame:
            drawRect(window, scoreBarColor, 0, gridSize, gridSize, scoreBoxH, -1, -1)
        else:
            drawRect(window, scoreBarMenuColor, 0, gridSize, gridSize, scoreBoxH, -1, -1)

        drawText(window, "Score: " + str(snake.length() - initSnakeLen), textColor, smallFont, 1 / 4, gridSize + scoreBoxH / 2, -1, 0)


    if not inGame and hasPlayed: # game over
        drawText(window, "Game Over!", textColor, font, gridSize / 2, gridSize / 2, 0, 0)
        
    if not inGame: # game over / start
        drawText(window, "Press Enter to Play", textColor, smallFont, gridSize / 2, gridSize * 0.6, 0, 0)

    if not inGame and not hasPlayed:
        pygame.draw.rect(window, scoreBarMenuColor, pygame.Rect(0, gridSize * scale, gridSize * scale, scoreBoxH))

        drawText(window, "SNAKE", textColor, font, gridSize / 2, gridSize / 2, 0, 0)
        
        drawText(window, "v" + version, textColor, smallFont, 1 / 4, gridSize + scoreBoxH / 2, -1, 0)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_RETURN and not inGame:
                inGame = True
                hasPlayed = True
                snake = Snake(gridSize / 2, gridSize / 2, initSnakeLen)
                mouse = Mouse(int(gridSize / 4), int(gridSize / 4))
                bloodstain = Bloodstain(gridSize, scale)
                key = 0
                dt = 0
                last = time.time() * 1000
            
    if key == pygame.K_LEFT or key == pygame.K_a:
        snake.changeDir(-1, 0)
    if key == pygame.K_RIGHT or key == pygame.K_d:
        snake.changeDir(1, 0)
    if key == pygame.K_UP or key == pygame.K_w:
        snake.changeDir(0, -1)
    if key == pygame.K_DOWN or key == pygame.K_s:
        snake.changeDir(0, 1)

    pygame.display.update()

    time.sleep(0.005)

