import math
import os
import time

import pygame
from pygame.locals import *
from pygame.draw import *

from copy import deepcopy

from Defenitions import *
import FruitType
from Ball import Ball

import numpy as np

configPath = os.path.dirname(os.path.realpath(__file__))
defaultWidth = 640
defaultHeight = 640
window = pygame.display.set_mode([defaultWidth, defaultHeight], RESIZABLE)
clock = pygame.time.Clock()
running = True

balls = [Ball(0.7, 0.2, 0.00, 0.01, FruitType.peach)]


def getScreenSize():
    return pygame.display.get_surface().get_size()


def textBlock(text: str, x: float, y: float, size: int, color: tuple | str, center: bool = True,
              absoluteSize: bool = True, font=None):
    if font is None:
        try:
            font = pygame.font.Font(configPath + "/ARCADECLASSIC.TTF", size)
        except Exception:
            print("file missing")
            font = pygame.font.SysFont("Arial", size)
        text = text.replace(' ', '     ')
    screenText = font.render(text, False, color)

    if absoluteSize:
        x, y = x * getScreenSize()[0], y * getScreenSize()[1]

    if center:
        x -= screenText.get_size()[0] // 2
        y -= screenText.get_size()[1] // 2
    window.blit(screenText, (x, y))


def longTextBlock(texts: list[str], x: float, y: float, size: int, color: tuple | str, center: bool = True,
                  absoluteSize: bool = True, sizeInPixels=True, font=None):
    realSize = size
    if not sizeInPixels:
        realSize = size * 16 // 12
    # split based on max length of text
    for i, text in enumerate(texts):
        print(texts)
        textBlock(text,
                  x,
                  y + 4 * i / realSize,
                  realSize,
                  color,
                  center,
                  absoluteSize,
                  font)


def exitGame():
    pygame.quit()
    exit()


def colisionSameType(i, j):
    newBall = Ball((balls[i].x + balls[j].x) / 2, (balls[i].y + balls[j].y) / 2, 0, 0,
                   balls[i].fruitType.nextFruitType)
    balls[i].hasColided = True
    balls[j].hasColided = True
    balls.append(newBall)



def colisionDifferentType(i, j):


    c1 = np.array([balls[i].x, balls[i].y])
    c2 = np.array([balls[j].x, balls[j].y])
    v1 = np.array([balls[i].velX, balls[i].velY])
    v2 = np.array([balls[j].velX, balls[j].velY])
    m1 = balls[i].radius
    m2 = balls[j].radius

    v1N = v1 - ((2 * m2) / (m1 + m2)) * (np.dot(v1 - v2, c1-c2)) / (math.dist((0,0), (c1-c2))) * (c1-c2)
    v2N = v2 - ((2 * m1) / (m2 + m1)) * (np.dot(v2 - v1, c2-c1)) / (math.dist((0,0), (c2-c1))) * (c2-c1)
    balls[i].velX = v1N[0]
    balls[i].velY = v1N[1]
    balls[j].velX = v2N[0]
    balls[j].velY = v2N[1]

    dx = balls[i].x - balls[j].x
    dy = balls[i].y - balls[j].y
    distance = balls[i].distance(balls[j])
    overlap = balls[i].radius + balls[j].radius - distance
    dx = dx / distance
    dy = dy / distance

    balls[i].x += dx * overlap / 2
    balls[i].y += dy * overlap / 2
    balls[j].x -= dx * overlap / 2
    balls[j].y -= dy * overlap / 2


    # normal = np.array([balls[i].x - xRR, balls[i].y - yRR])
    # normal = normal / (math.dist((0,0), normal))
    # tangent = np.array([-normal[1], normal[0]])
    #
    #
    # vel1N = normal * v2
    # vel1T = tangent * v1
    # vel2N = normal * v2
    # vel2T = tangent * v2
    #
    #
    #
    # vel1NScalar = ((math.dist((0,0), vel1N)) * (m1-m2) + 2 * m1 * (math.dist((0,0), vel2N))) / (m1 + m2)
    # vel2NScalar = ((math.dist((0,0), vel2N)) * (m2-m1) + 2 * m2 * (math.dist((0,0), vel1N))) / (m2 + m1)
    #
    # vel1NNew = vel1NScalar * normal
    # vel2NNew = vel2NScalar * normal
    #
    # vel1New = vel1NNew + vel1T
    # vel2New = vel2NNew + vel2T
    #
    # print(v1,vel1New)
    #
    # balls[i].velX = vel1New[0]
    # balls[i].velY = vel1New[1]
    # balls[j].velX = vel2New[0]
    # balls[j].velY = vel2New[1]
    #
    # balls[i].x += dx * overlap / 1.9
    # balls[i].y += dy * overlap / 1.9
    # balls[j].x -= dx * overlap / 1.9
    # balls[j].y -= dy * overlap / 1.9

    pygame.display.flip()

    # update speed of both balls when they collide
    # balls[i].velY = 0
    # balls[j].velY = 0


def handleColision():
    global balls
    for i in range(len(balls)):
        if not balls[i].hasColided:
            for j in range(i + 1, len(balls)):
                if not balls[j].hasColided:
                    if balls[i].collision(balls[j]) and balls[i].fruitType.nextFruitType is not None and balls[
                        i].fruitType == balls[j].fruitType:
                        colisionSameType(i, j)
                    elif balls[i].collision(balls[j]):
                        colisionDifferentType(i, j)

    balls = [ball for ball in balls if not ball.hasColided]


first = True
start = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(Ball(pygame.mouse.get_pos()[0] / screenSize[0], 0.2, 0.00, 0.01, FruitType.peach))
    keys = pygame.key.get_pressed()
    timeDelta = clock.tick(FPS) / 1000
    screenSize = getScreenSize()
    handleColision()

    window.fill((0, 0, 0))
    for ball in balls:
        ball.update(timeDelta)
        ball.draw(window, screenSize)


    pygame.display.flip()
