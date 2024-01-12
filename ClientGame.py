import os

import pymunk

import Client
import pygame
from pygame.locals import *
from pygame.draw import *
import pygame_gui
import pymunk
import Definitions
from Definitions import *
import time
from typing import List
from Protocol import RequestType, ApplicationError

import random

import FruitType
from Ball import Ball
from Definitions import *



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


def getRelativePosition():
    return pygame.mouse.get_pos()[0] / getScreenSize(), pygame.mouse.get_pos()[1] / \
           getScreenSize()


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
        x, y = x * getScreenSize() + xPadding, y * getScreenSize() + yPadding

    if center:
        x -= screenText.get_size()[0] // 2
        y -= screenText.get_size()[1] // 2
    window.blit(screenText, (x, y))


def longTextBlock(texts: list[str], x: float, y: float, size: int, color: tuple | str, center: bool = True,
                  absoluteSize: bool = True, sizeInPixels=True,font=None):
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
    try:
        Client.send(RequestType.DISCONNECT)
    except OSError:
        pass
    pygame.quit()
    exit()

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
    colidedBall = Ball(newX, newY, ammountGenerated, FruitType.fruitTypes[data + 1])
    addPoints(colidedBall.fruitType.points)
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
    nextFruit = Ball(nextFruitX, 0, ammountGenerated, nextFruitType)
    addPoints(nextFruit.fruitType.points)
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
    if isPlayer:
        for ball in balls:
            # ball.update(timeDelta)
            ball.draw(window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize)

        if time.time() - delayStart > delayTime:
            Ball.drawBall(max(min((pygame.mouse.get_pos()[0] - ZERO_X) / (ONE_X - ZERO_X),
                                  1 - nextFruitType.radius),
                              0 + nextFruitType.radius), 0, nextFruitType, window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize)
    else:
        for ball in opBalls:
            # ball.update(timeDelta)
            ball.draw(window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize)
    textBlock("points " + str(points), 0, 0, 20, 'white', False, True, pygame.font.SysFont("Arial", 20))

    pygame.display.flip()

points = 0
delayTime = 0.5
delayStart = time.time() - delayTime

isPlayer = True
opBalls = []
def addPoints(np):
    global points
    points += np

def getOpponentBalls():
    return [Ball(0.25, 0.75, ammountGenerated, FruitType.cherry),Ball(0.75, 0.25, ammountGenerated, FruitType.cherry)]
def getOpponentSpace():
    return setupSpace(opBalls)

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
hub = True


balls = []
space = setupSpace(balls)
opSpace = None

screenSize = getScreenSize()
first = True
start = time.time()

nextFruitType = random.choice(FruitType.fruitTypes[:4])

ammountGenerated = 0
for i in range(0, 9):
    handler = space.add_collision_handler(i, i)
    handler.begin = (lambda arbiter, space, data, i=i: handleCollision(arbiter, space, i))

# server is down
while not Client.isConnected:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
    keys = pygame.key.get_pressed()
    clock.tick(FPS)
    window.fill((0, 0, 0))
    longTextBlock(
        [f"Server {str(Client.ADDR)} is down", "please close the application and", "open it again at a later time"],
        0.5,
        0.3,
        getScreenSize() // 30,
        "white",
        font=pygame.font.SysFont("Arial", getScreenSize() // 30))
    pygame.display.flip()
try:
    games = Client.sendAndRecv(RequestType.RETRIEVE_GAMES).value

    # TODO menu, button for creating games, list of current games to join, textbox to enter password, pause menu (with
    #  compatibility with server)


    # Cardinality = Client.send(RequestType.JOIN_GAME, {"name": "chen", "password": None}).value


    manager = pygame_gui.UIManager([defaultWidth, defaultHeight])
    CreateGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0 + xPadding, getScreenSize() - 50 + yPadding), (130, 50 + yPadding)),
                                                    text='Create Game',
                                                    manager=manager)
    RefreshButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130 + xPadding, getScreenSize() - 50 + yPadding), (130, 50 + yPadding)),
                                                 text='Refresh',
                                                 manager=manager)
    NameTextBox = pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((getScreenSize() / 2 - 65 + xPadding, getScreenSize() / 2 - 85 + yPadding), (130, 50 + yPadding)),
        manager=manager)
    PasswordTextBox = pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((getScreenSize() / 2 - 65 + xPadding, getScreenSize() / 2 - 25 + yPadding), (130, 50 + yPadding)),
        manager=manager)
    OKButton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((getScreenSize() / 2 + 65 + xPadding, getScreenSize() / 2 + 25 + yPadding), (65, 50 + yPadding)),
        text='OK',
        manager=manager)
    CancelButton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((getScreenSize() / 2 + 130 + xPadding, getScreenSize() / 2 + 25 + yPadding), (65, 50 + yPadding)),
        text='Cancel',
        manager=manager)
    gameButtons = [pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0 + xPadding, getScreenSize() / 5 + 50 * i + yPadding), (getScreenSize(), 50 + yPadding)),
        text=game,
        manager=manager) for i, game in enumerate(games)]
    CancelButton.hide()
    OKButton.hide()
    NameTextBox.hide()
    PasswordTextBox.hide()
    request = None
    joinGameName = None

    # show game
    print(f"{Client.isConnected=}")
    while hub:
        timeDelta = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == CreateGameButton:
                    CancelButton.show()
                    OKButton.show()
                    NameTextBox.show()
                    NameTextBox.set_text('')
                    PasswordTextBox.show()
                    PasswordTextBox.set_text('')
                    CreateGameButton.disable()
                    RefreshButton.disable()
                    for button in gameButtons:
                        button.disable()
                    request = RequestType.CREATE_GAME
                if event.ui_element == CancelButton:
                    CancelButton.hide()
                    OKButton.hide()
                    NameTextBox.hide()
                    PasswordTextBox.hide()
                    CreateGameButton.enable()
                    RefreshButton.enable()
                    for button in gameButtons:
                        button.enable()
                if event.ui_element == OKButton:
                    if request == RequestType.CREATE_GAME:
                        Cardinality = Client.sendAndRecv(request, {"name": NameTextBox.get_text(),
                                                                   "password": PasswordTextBox.get_text()}).value
                    elif request == RequestType.JOIN_GAME:
                        print(PasswordTextBox.get_text())
                        Cardinality = Client.sendAndRecv(request, {"name": joinGameName,
                                                                   "password": PasswordTextBox.get_text()}).value
                    Client.sendAndRecv(RequestType.RETRIEVE_GAMES).print(True)
                    CreateGameButton.kill()
                    RefreshButton.kill()
                    CancelButton.kill()
                    OKButton.kill()
                    NameTextBox.kill()
                    PasswordTextBox.kill()
                    for button in gameButtons:
                        button.kill()
                    hub = False
                if event.ui_element in gameButtons:
                    CancelButton.show()
                    OKButton.show()
                    PasswordTextBox.show()
                    PasswordTextBox.set_text('')
                    CreateGameButton.disable()
                    RefreshButton.disable()
                    for button in gameButtons:
                        button.disable()
                    request = RequestType.JOIN_GAME
                    joinGameName = event.ui_element.text
                if event.ui_element == RefreshButton:
                    games = Client.sendAndRecv(RequestType.RETRIEVE_GAMES).value
                    for button in gameButtons:
                        button.kill()
                    gameButtons = [pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((0, getScreenSize() / 5 + 50 * i), (getScreenSize(), 50)),
                        text=game,
                        manager=manager) for i, game in enumerate(games)]
            manager.process_events(event)
        manager.update(timeDelta)
        manager.draw_ui(window)
        pygame.display.flip()
        window.fill((0, 0, 0))
    print(Cardinality)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if time.time() - delayStart > delayTime and event.button == 1 and isPlayer:  # left click
                    delayStart = time.time()
                    generateNewFruit()
                elif event.button == 3:  # right click
                    isPlayer = not isPlayer
                    opBalls = getOpponentBalls()
                    opSpace = setupSpace(opBalls)
        keys = pygame.key.get_pressed()
        timeDelta = clock.tick(FPS) / 1000
        space.step(timeDelta)
        if not isPlayer:
            opSpace.step(timeDelta)
        updateScreen()
except ApplicationError as e:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
        keys = pygame.key.get_pressed()
        clock.tick(FPS)
        textBlock("ERROR SCREEN", 0.5, 0.1, 40, "white",font=pygame.font.SysFont("Arial", 40))
        textBlock(str(e), 0.5, 0.5, 25, "white",font=pygame.font.SysFont("Arial", 25))
        pygame.display.flip()
        window.fill((255, 0, 0))
exitGame()
