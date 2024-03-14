import os
import time

import pygame

from pygame.draw import *
from pygame.locals import *

from Definitions import *

pygame.init()

# Define constants
configPath = os.path.dirname(os.path.realpath(__file__))
defaultWidth = 640 * 16 / 9
defaultHeight = 640
screenSize = min(defaultWidth, defaultHeight)

# makes the screen efectively a square by adding these values regardless of size
# recalculated at resize
xPadding = (defaultWidth - screenSize) / 2
yPadding = (defaultHeight - screenSize) / 2

# The frame of the game: ZERO_X is the point at which the box starts etc.
# This frame can later be moved around
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

    ONE_X = (screenPercents[0] / 2) * _screenSize + xPadding
    ZERO_X = (-screenPercents[0] / 2) * _screenSize + xPadding
    ONE_Y = (0.5 + screenPercents[1] / 2) * _screenSize + yPadding
    ZERO_Y = (0.5 - screenPercents[1] / 2) * _screenSize + yPadding

    return _screenSize


def textBlock(text: str, x: float, y: float, size: int, color: tuple | str, center: bool = True,
              absoluteSize: bool = True, font=None):
    if font is None:
        try:
            font = pygame.font.Font(configPath + "\\ARCADECLASSIC.TTF", size)
        except FileNotFoundError:
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
    collided = []
    for shape in arbiter.shapes:
        for ball in balls:
            if ball.shape == shape:
                collided.append(ball)
    balls.remove(collided[0])
    balls.remove(collided[1])
    space.remove(collided[0].shape)
    space.remove(collided[1].shape)

    newX, newY = (collided[0].body.position.x + collided[1].body.position.x) / 2, (
            collided[0].body.position.y + collided[1].body.position.y) / 2
    colidedBall = Ball(newX, newY, FruitType.fruitTypes[data + 1])
    addPoints(colidedBall.fruitType.points)
    colidedBall.addObject(space)
    balls.append(colidedBall)

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
    mousePosition = clamp(pygame.mouse.get_pos()[0], ZERO_X + nextFruitType.radius * (ONE_X - ZERO_X), ONE_X - nextFruitType.radius * (ONE_X - ZERO_X))
    mousePercent = ((mousePosition - ZERO_X) / (ONE_X - ZERO_X))
    nextFruit = Ball(mousePercent, 0, nextFruitType)
    addPoints(nextFruit.fruitType.points)
    nextFruit.addObject(space)
    balls.append(nextFruit)
    nextFruitType = random.choice(FruitType.fruitTypes[:4])


def drawPlayerBox():
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


def drawOpponentBox():
    line(window, 'white',
         ((screenSize - ZERO_X) + ONE_X, ZERO_Y),
         ((screenSize - ZERO_X) + ONE_X, ONE_Y),
         5)
    line(window, 'white',
         ((screenSize - ZERO_X) + ZERO_X, ZERO_Y),
         ((screenSize - ZERO_X) + ZERO_X, ONE_Y),
         5)
    line(window, 'white',
         ((screenSize - ZERO_X) + ZERO_X, ONE_Y),
         ((screenSize - ZERO_X) + ONE_X, ONE_Y),
         5)


def updateScreen():
    screenSize = getScreenSize()

    window.fill((0, 0, 0))
    drawPlayerBox()
    drawOpponentBox()
    circle(window,'red',(ZERO_X,ZERO_Y), 5)
    circle(window,'red',(ZERO_X,ONE_Y), 5)
    circle(window,'red',(ONE_X,ZERO_Y), 5)
    circle(window,'red',(ONE_X,ONE_Y), 5)

    for ball in balls:
        # ball.update(timeDelta)
        ball.draw(window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize)

    if time.time() - delayStart > delayTime:
        # mouse clamp position to window
        mousePosition = clamp(pygame.mouse.get_pos()[0], ZERO_X + nextFruitType.radius * (ONE_X - ZERO_X), ONE_X - nextFruitType.radius * (ONE_X - ZERO_X))
        mousePercent = ((mousePosition - ZERO_X) / (ONE_X - ZERO_X))
        Ball.drawBall(mousePercent, 0, nextFruitType, window, ZERO_X, ONE_X, ZERO_Y, ONE_Y,
                      screenSize)
    for ball in opBalls:
        # ball.update(timeDelta)
        ball.draw(window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize)
    textBlock("points " + str(points), 0, 0, 20, 'white', False, True, pygame.font.SysFont("Arial", 20))

    pygame.display.flip()


def exitGame():
    pygame.quit()
    exit()


points = 0
delayTime = 0.5
delayStart = time.time() - delayTime

opBalls = []


def addPoints(np):
    global points
    points += np


def getOpponentBalls():
    return [Ball(0.25, 0.75, FruitType.cherry), Ball(0.75, 0.25, FruitType.cherry)]


def getOpponentSpace():
    return setupSpace(opBalls)


balls = []
space = setupSpace(balls)

screenSize = getScreenSize()
first = True
start = time.time()

nextFruitType = random.choice(FruitType.fruitTypes[:4])

for i in range(0, 9):
    handler = space.add_collision_handler(i, i)
    handler.begin = (lambda arbiter, space, data, i=i: handleCollision(arbiter, space, i))

# TODO: Get opponent balls
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if time.time() - delayStart > delayTime and event.button == 1:  # left click
                delayStart = time.time()
                generateNewFruit()
    keys = pygame.key.get_pressed()
    timeDelta = clock.tick(FPS) / 1000
    space.step(timeDelta)
    updateScreen()
