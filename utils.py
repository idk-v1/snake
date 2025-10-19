import sys
import pygame
import random
import time
import math

scale = 60

def toRad(deg):
    return deg / 180.0 * math.pi

def rotPoint(cx, cy, length, deg):
    x = math.cos(toRad(deg)) * length + cx
    y = math.sin(toRad(deg)) * length + cy
    return (x, y)


def drawText(window, string, color, font, x, y, ax, ay):
    textSize = font.size(string)
    text = font.render(string, True, color)
    tx = x * scale - textSize[0] / 2 - ax * textSize[0] / 2
    ty = y * scale - textSize[1] / 2 - ay * textSize[1] / 2
    window.blit(text, (tx, ty))

def drawCircle(window, color, x, y, rad):
    pygame.draw.circle(window, color, (x * scale, y * scale), int(rad * scale))

def drawLinePt(window, color, sx, sy, ex, ey, width):
    pygame.draw.line(window, color, (sx * scale, sy * scale), (ex * scale, ey * scale), int(width * scale))

def drawLineRot(window, color, cx, cy, length, deg, width):
    endPt = rotPoint(cx, cy, length, deg)
    drawLinePt(window, color, cx, cy, endPt[0], endPt[1], width)

def drawRect(window, color, x, y, w, h, ax, ay):
    tx = x - w / 2 - ax * w / 2
    ty = y - h / 2 - ay * h / 2
    pygame.draw.rect(window, color, (tx * scale, ty * scale, w * scale, h * scale))
