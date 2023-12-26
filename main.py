import os
import time

import pygame
import pymunk
from pygame.draw import *
from pygame.locals import *

import random

import FruitType
from Ball import Ball
from Defenitions import *

configPath = os.path.dirname(os.path.realpath(__file__))
defaultWidth = 640 * 16 / 9
defaultHeight = 640
xPadding = max(defaultWidth - defaultHeight, 0) / 2
yPadding = max(defaultHeight - defaultWidth, 0) / 2
window = pygame.display.set_mode([defaultWidth, defaultHeight], RESIZABLE)
clock = pygame.time.Clock()
running = True

biggestIndex = 0


def getScreenSize():
    global xPadding
    global yPadding
    defaultWidth, defaultHeight = pygame.display.get_surface().get_size()
    xPadding = max(defaultWidth - defaultHeight, 0) / 2
    yPadding = max(defaultHeight - defaultWidth, 0) / 2
    return min(defaultWidth, defaultHeight)


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
    colidedBall = Ball(newX, newY, ammountGenerated, FruitType.fruitTypes[data + 1])
    colidedBall.addObject(space)
    balls.append(colidedBall)
    ammountGenerated += 1

    return True


def exitGame():
    pygame.quit()
    exit()


space = pymunk.Space()
space._set_collision_slop(0)
space.gravity = (0, Gravity)
# floor
body = pymunk.Body(body_type=pymunk.Body.STATIC)
shape = pymunk.Segment(body, (0.5 - screenPercents[0] / 2, 0.5 + screenPercents[1] / 2),
                       (0.5 + screenPercents[0] / 2, 0.5 + screenPercents[1] / 2), 0.01)
shape.collision_type = 99999999
space.add(body, shape)

# left Wall
body = pymunk.Body(body_type=pymunk.Body.STATIC)
shape = pymunk.Segment(body, (0.5 - screenPercents[0] / 2, 0.5 - screenPercents[1] / 2),
                       (0.5 - screenPercents[0] / 2, 0.5 + screenPercents[1] / 2), 0.01)
shape.collision_type = 99999999
space.add(body, shape)

# right Wall
body = pymunk.Body(body_type=pymunk.Body.STATIC)
shape = pymunk.Segment(body, (0.5 + screenPercents[0] / 2, 0.5 - screenPercents[1] / 2),
                       (0.5 + screenPercents[0] / 2, 0.5 + screenPercents[1] / 2), 0.01)
shape.collision_type = 99999999
space.add(body, shape)

screenSize = getScreenSize()
first = True
start = time.time()

nextFruit = Ball(0.8, 0.2, -1, random.choice(FruitType.fruitTypes[:4]))

balls = []
ammountGenerated = 0
handler = space.add_collision_handler(0, 0)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 0))
handler = space.add_collision_handler(1, 1)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 1))
handler = space.add_collision_handler(2, 2)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 2))
handler = space.add_collision_handler(3, 3)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 3))
handler = space.add_collision_handler(4, 4)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 4))
handler = space.add_collision_handler(5, 5)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 5))
handler = space.add_collision_handler(6, 6)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 6))
handler = space.add_collision_handler(7, 7)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 7))
handler = space.add_collision_handler(8, 8)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 8))
handler = space.add_collision_handler(9, 9)
handler.begin = (lambda arbiter, space, data: handleCollision(arbiter, space, 9))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
        if event.type == pygame.MOUSEBUTTONDOWN:
            nextFruitX = max(min((pygame.mouse.get_pos()[0] - xPadding) / screenSize,
                                 0.5 + screenPercents[0] / 2 - nextFruit.shape.radius),
                             0.5 - screenPercents[0] / 2 + nextFruit.shape.radius)
            nextFruit = Ball(nextFruitX, 0.2, ammountGenerated, nextFruit.fruitType)
            nextFruit.addObject(space)
            balls.append(nextFruit)
            nextFruit = Ball(0.8, 0.2, ammountGenerated, random.choice(FruitType.fruitTypes[:4]))
            ammountGenerated += 1
    keys = pygame.key.get_pressed()
    timeDelta = clock.tick(FPS) / 1000
    space.step(timeDelta)
    screenSize = getScreenSize()

    window.fill((0, 0, 0))
    line(window, 'white',
         (xPadding + (0.5 + screenPercents[0] / 2) * screenSize, yPadding + (0.5 - screenPercents[1] / 2) * screenSize),
         (xPadding + (0.5 + screenPercents[0] / 2) * screenSize, yPadding + (0.5 + screenPercents[1] / 2) * screenSize),
         5)
    line(window, 'white',
         (xPadding + (0.5 - screenPercents[0] / 2) * screenSize, yPadding + (0.5 - screenPercents[1] / 2) * screenSize),
         (xPadding + (0.5 - screenPercents[0] / 2) * screenSize, yPadding + (0.5 + screenPercents[1] / 2) * screenSize),
         5)
    line(window, 'white',
         (xPadding + (0.5 - screenPercents[0] / 2) * screenSize, yPadding + (0.5 + screenPercents[1] / 2) * screenSize),
         (xPadding + (0.5 + screenPercents[0] / 2) * screenSize, yPadding + (0.5 + screenPercents[1] / 2) * screenSize),
         5)
    for ball in balls:
        # ball.update(timeDelta)
        ball.draw(window, screenSize, xPadding, yPadding)
    nextFruit.draw(window, screenSize, xPadding, yPadding)

    pygame.display.flip()
