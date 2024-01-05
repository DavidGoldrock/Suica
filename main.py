import os
import time
from typing import List

import pygame
import pymunk
from pygame.draw import *
from pygame.locals import *

import random

import FruitType
from Ball import Ball
from Defenitions import *

pygame.init()

configPath = os.path.dirname(os.path.realpath(__file__))
defaultWidth = 640 * 16 / 9
defaultHeight = 640
screenSize = min(defaultWidth, defaultHeight)
xPadding = (defaultWidth - screenSize) / 2
yPadding = (defaultHeight - screenSize) / 2

ONE_X = (0.5 + screenPercents[0] / 2) * screenSize + xPadding
ZERO_X = (0.5 - screenPercents[0] / 2) * screenSize + xPadding
ONE_Y = (0.5 + screenPercents[1] / 2) * screenSize + yPadding
ZERO_Y = (0.5 - screenPercents[1] / 2) * screenSize + yPadding

window = pygame.display.set_mode([defaultWidth, defaultHeight], RESIZABLE)
clock = pygame.time.Clock()
running = True
biggestIndex = 0


def getScreenSize():
    global defaultWidth
    global defaultHeight
    global xPadding
    global yPadding
    global ONE_X
    global ZERO_X
    global ONE_Y
    global ZERO_Y
    defaultWidth, defaultHeight = pygame.display.get_surface().get_size()
    _screenSize = min(defaultWidth, defaultHeight)
    xPadding = (defaultWidth - _screenSize) / 2
    yPadding = (defaultHeight - _screenSize) / 2

    ONE_X = (0.5 + screenPercents[0] / 2) * _screenSize + xPadding
    ZERO_X = (0.5 - screenPercents[0] / 2) * _screenSize + xPadding
    ONE_Y = (0.5 + screenPercents[1] / 2) * _screenSize + yPadding
    ZERO_Y = (0.5 - screenPercents[1] / 2) * _screenSize + yPadding

    return _screenSize


def textBlock(text: str, x: float, y: float, size: int, color: tuple | str, center: bool = True,
              absoluteSize: bool = True, font=None):
    if font is None:
        try:
            font = pygame.font.Font(configPath + "\\ARCADECLASSIC.TTF", size)
        except Exception:
            print("file missing")
            font = pygame.font.SysFont("Arial", size)
        text = text.replace(' ', '     ')
    screenText = font.render(text, False, color)

    if absoluteSize:
        x, y = x * getScreenSize(), y * getScreenSize()

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


def handleCollision(arbiter, space, data):
    print(data)
    global ammountGenerated
    colided = []
    for shape in arbiter.shapes:
        for ball in balls:
            if ball.shape == shape:
                colided.append(ball)
    balls.remove(colided[0])
    balls.remove(colided[1])
    space.remove(colided[0].shape)
    space.remove(colided[1].shape)

    newX, newY = (colided[0].body.position.x + colided[1].body.position.x) / 2, (
            colided[0].body.position.y + colided[1].body.position.y) / 2
    colidedBall = Ball(newX, newY, ammountGenerated, FruitType.fruitTypes[data + 1], addPoints)
    colidedBall.addObject(space)
    balls.append(colidedBall)
    ammountGenerated += 1

    return True


def setupSpace(balls: List[Ball]):
    space = pymunk.Space()
    space.collision_slop = 0
    space.gravity = (0, Gravity)

    # setup box
    # floor
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (0, 1),
                           (1, 1), 0.01)
    shape.collision_type = 99999999
    space.add(body, shape)

    # left Wall
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (0, 0),
                           (0, 1), 0.01)
    shape.collision_type = 99999999
    space.add(body, shape)

    # right Wall
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (1, 0),
                           (1, 1), 0.01)
    shape.collision_type = 99999999
    space.add(body, shape)

    for ballToAdd in balls:
        ballToAdd.addObject(space)

    return space

def generateNewFruit():
    global nextFruitType
    global balls
    global ammountGenerated
    nextFruitX = max(min((pygame.mouse.get_pos()[0] - ZERO_X) / (ONE_X - ZERO_X),
                         1 - nextFruitType.radius),
                     0 + nextFruitType.radius)
    nextFruit = Ball(nextFruitX, 0, ammountGenerated, nextFruitType, addPoints)
    nextFruit.addObject(space)
    balls.append(nextFruit)
    ammountGenerated += 1
    nextFruitType = random.choice(FruitType.fruitTypes[:4])


def drawBox():
    global screenSize
    screenSize = getScreenSize()
    line(window, 'white',
         (ONE_X, ZERO_Y),
         (ONE_X, ONE_Y),
         5)
    line(window, 'white',
         (ZERO_X, ZERO_Y),
         (ZERO_X, ONE_Y),
         5)
    line(window, 'white',
         (ZERO_X, ONE_Y),
         (ONE_X, ONE_Y),
         5)

def updateScreen():
    screenSize = getScreenSize()

    window.fill((0, 0, 0))
    drawBox()
    for ball in balls:
        # ball.update(timeDelta)
        ball.draw(window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize)

    if time.time() - delayStart > delayTime:
        Ball.drawBall(max(min((pygame.mouse.get_pos()[0] - ZERO_X) / (ONE_X - ZERO_X),
                              1 - nextFruitType.radius),
                          0 + nextFruitType.radius), 0, nextFruitType, window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize)
    textBlock("points " + str(points), 0, 0, 20, 'white', False, True, pygame.font.SysFont("Arial", 20))

    pygame.display.flip()


def exitGame():
    pygame.quit()
    exit()


points = 0
delayTime = 0.5
delayStart = time.time() - delayTime


def addPoints(np):
    global points
    points += np


balls = []
space = setupSpace(balls)

screenSize = getScreenSize()
first = True
start = time.time()

nextFruitType = random.choice(FruitType.fruitTypes[:4])

ammountGenerated = 0
for i in range(0,9):
    handler = space.add_collision_handler(i, i)
    handler.begin = (lambda arbiter, space, data, i=i: handleCollision(arbiter, space, i))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
        if event.type == pygame.MOUSEBUTTONDOWN and time.time() - delayStart > delayTime:
            delayStart = time.time()
            generateNewFruit()
    keys = pygame.key.get_pressed()
    timeDelta = clock.tick(FPS) / 1000
    space.step(timeDelta)
    updateScreen()
