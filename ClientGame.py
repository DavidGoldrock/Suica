import os

import Client
import pygame
from pygame.locals import *
from pygame.draw import *
import pygame_gui
import time
from Protocol import RequestType, ApplicationError
from Definitions import *
import FruitType

# Default values
Cardinality = 0

# Screem Values
defaultWidth = 640 * 16 / 9
defaultHeight = 640
screenSize = min(defaultWidth, defaultHeight)
xPadding = (defaultWidth - screenSize) / 2
yPadding = (defaultHeight - screenSize) / 2

# Box points, seperated by Player 1 and 2
ONE_X_P1 = (0.5 + screenPercents[0] / 2) * screenSize + xPadding
ZERO_X_P1 = (0.5 - screenPercents[0] / 2) * screenSize + xPadding
ONE_X_P2 = (screenSize - ZERO_X_P1) + (0.5 + screenPercents[0] / 2) * screenSize + xPadding
ZERO_X_P2 = (screenSize - ZERO_X_P1) + (0.5 - screenPercents[0] / 2) * screenSize + xPadding
ONE_Y = (0.5 + screenPercents[1] / 2) * screenSize + yPadding
ZERO_Y = (0.5 - screenPercents[1] / 2) * screenSize + yPadding


def getScreenSize():
    """
    every Resize this function resets all screen values
    :return: the minimum between the width and the height of the window
    """
    global defaultWidth
    global defaultHeight
    global xPadding
    global yPadding
    global ONE_X_P1
    global ZERO_X_P1
    global ONE_X_P2
    global ZERO_X_P2
    global ONE_Y
    global ZERO_Y
    defaultWidth, defaultHeight = pygame.display.get_surface().get_size()
    _screenSize = min(defaultWidth, defaultHeight)
    xPadding = (defaultWidth - _screenSize) / 2
    yPadding = (defaultHeight - _screenSize) / 2

    ONE_X_P1 = (screenPercents[0] / 2) * _screenSize + xPadding
    ZERO_X_P1 = (-screenPercents[0] / 2) * _screenSize + xPadding
    ONE_X_P2 = (_screenSize - ZERO_X_P1) + ONE_X_P1
    ZERO_X_P2 = (_screenSize - ZERO_X_P1) + ZERO_X_P1
    ONE_Y = (0.5 + screenPercents[1] / 2) * _screenSize + yPadding
    ZERO_Y = (0.5 - screenPercents[1] / 2) * _screenSize + yPadding

    return _screenSize


def getClampedMouse(Cardinality: int):
    """
    clamps the position of the mouse with the box of the player
    compensates for the radius of the fruit
    returns as percent
    :param Cardinality: whether it is player 1 or 2
    :return: the point of the mouse clamped by the player's box
    """
    if Cardinality == 0:
        mousePosition = clamp(pygame.mouse.get_pos()[0], ZERO_X_P1 + nextFruitType.radius * (ONE_X_P1 - ZERO_X_P1),
                              ONE_X_P1 - nextFruitType.radius * (ONE_X_P1 - ZERO_X_P1))
        mousePercent = ((mousePosition - ZERO_X_P1) / (ONE_X_P1 - ZERO_X_P1))
        return mousePercent

    else:
        mousePosition = clamp(pygame.mouse.get_pos()[0], ZERO_X_P2 + nextFruitType.radius * (ONE_X_P2 - ZERO_X_P2),
                              ONE_X_P2 - nextFruitType.radius * (ONE_X_P2 - ZERO_X_P2))
        mousePercent = ((mousePosition - ZERO_X_P2) / (ONE_X_P2 - ZERO_X_P2))
        return mousePercent


def textBlock(text: str, x: float, y: float, size: int, color: tuple | str, center: bool = True,
              absoluteSize: bool = True, font=None):
    """
    writes text to screen
    :param text: text to write
    :param x: x position of the text
    :param y: y position of the text
    :param size: size of the text in pixels / percent
    :param color: color of the text: string or rgb tuple
    :param center: should the position be of the center of the text or the top left point. default is center
    :param absoluteSize: should the size be given as percent or pixels. default is percent
    :param font: custom font object, default is the ARCADECLASSIC.TTF that comes with the game
    """
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
    """
    writes text to screen
    :param texts:
    :param x: x position of the text
    :param y: y position of the text
    :param color: color of the text: string or rgb tuple
    :param center: should the position be of the center of the text or the top left point. default is center
    :param absoluteSize: should the size be given as percent or pixels. default is percent
    :param size: size of the text in pixels / percent
    :param sizeInPixels: in case you wanna put the size as word size? IDK if I should remove this
    :param font: custom font object, default is the ARCADECLASSIC.TTF that comes with the game
    """
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
    """
    sends message to the server of quit and closes window
    """
    try:
        Client.send(RequestType.DISCONNECT)
    except OSError:
        pass
    pygame.quit()
    exit()


def drawPlayer1Box():
    """
    draws player 1 box
    """
    global screenSize
    screenSize = getScreenSize()
    line(window, 'white',
         (ONE_X_P1, ZERO_Y),
         (ONE_X_P1, ONE_Y),
         5)
    line(window, 'white',
         (ZERO_X_P1, ZERO_Y),
         (ZERO_X_P1, ONE_Y),
         5)
    line(window, 'white',
         (ZERO_X_P1, ONE_Y),
         (ONE_X_P1, ONE_Y),
         5)


def drawPlayer2Box():
    """
    draws player 2 box
    """
    line(window, 'white',
         (ONE_X_P2, ZERO_Y),
         (ONE_X_P2, ONE_Y),
         5)
    line(window, 'white',
         (ZERO_X_P2, ZERO_Y),
         (ZERO_X_P2, ONE_Y),
         5)
    line(window, 'white',
         (ZERO_X_P2, ONE_Y),
         (ONE_X_P2, ONE_Y),
         5)


def updateScreen(currentGameVars):
    """
    does all drawing to screen
    :param currentGameVars: Defenitions.Game object of the current game vars
    """
    # Resets screenSize
    global screenSize
    screenSize = getScreenSize()

    # clear screen
    window.fill((0, 0, 0))

    # draw the boxes
    drawPlayer1Box()
    drawPlayer2Box()

    # Debugging drawing
    circle(window, 'red', (ZERO_X_P1, ZERO_Y), 5)
    circle(window, 'red', (ZERO_X_P1, ONE_Y), 5)
    circle(window, 'red', (ONE_X_P1, ZERO_Y), 5)
    circle(window, 'red', (ONE_X_P1, ONE_Y), 5)
    circle(window, 'red', (getClampedMouse(0) * (ONE_X_P1 - ZERO_X_P1) + ZERO_X_P1, ONE_Y), 5)

    circle(window, 'green', (ZERO_X_P2, ZERO_Y), 5)
    circle(window, 'green', (ZERO_X_P2, ONE_Y), 5)
    circle(window, 'green', (ONE_X_P2, ZERO_Y), 5)
    circle(window, 'green', (ONE_X_P2, ONE_Y), 5)
    circle(window, 'green', (getClampedMouse(1) * (ONE_X_P2 - ZERO_X_P2) + ZERO_X_P2, ONE_Y), 5)

    # draws all balls
    for ball in currentGameVars.player1Balls:
        ball.draw(window, ZERO_X_P1, ONE_X_P1, ZERO_Y, ONE_Y, screenSize)

    for ball in currentGameVars.player2Balls:
        ball.draw(window, ZERO_X_P2, ONE_X_P2, ZERO_Y, ONE_Y, screenSize)

    # If the cooldown from the last fruit ended
    if time.time() - delayStart > delayTime:
        # mouse clamp position to window
        mousePercent = getClampedMouse(Cardinality)

        # draw ball in the correct box
        if Cardinality == 0:
            Ball.drawBall(mousePercent, 0, nextFruitType, window, ZERO_X_P1, ONE_X_P1, ZERO_Y, ONE_Y,
                          screenSize)
        else:
            Ball.drawBall(mousePercent, 0, nextFruitType, window, ZERO_X_P2,
                          ONE_X_P2, ZERO_Y, ONE_Y,
                          screenSize)
    # choose correct points
    if Cardinality == 0:
        points = currentGameVars.player1Score
    else:
        points = currentGameVars.player2Score

    textBlock("points " + str(points), 0, 0, 20, 'white', False, True, pygame.font.SysFont("Arial", 20))

    pygame.display.flip()


pygame.init()

# time to delay between fruits
delayTime = 0.5
delayStart = time.time() - delayTime

# path to current directory
configPath = os.path.dirname(os.path.realpath(__file__))

window = pygame.display.set_mode([defaultWidth, defaultHeight], RESIZABLE)
clock = pygame.time.Clock()

# is in create game / join game screen
hub = True
# is game on
running = True

# update screenSize
screenSize = getScreenSize()

# the fruit Type of the next ball the player will drop
nextFruitType = random.choice(FruitType.fruitTypes[:4])

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


    manager = pygame_gui.UIManager((int(defaultWidth), defaultHeight))
    CreateGameButton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0 + xPadding, getScreenSize() - 50 + yPadding), (130, 50 + yPadding)),
        text='Create Game',
        manager=manager)
    RefreshButton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((130 + xPadding, getScreenSize() - 50 + yPadding), (130, 50 + yPadding)),
        text='Refresh',
        manager=manager)
    NameTextBox = pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((getScreenSize() / 2 - 65 + xPadding, getScreenSize() / 2 - 85 + yPadding),
                                  (130, 50 + yPadding)),
        manager=manager)
    PasswordTextBox = pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((getScreenSize() / 2 - 65 + xPadding, getScreenSize() / 2 - 25 + yPadding),
                                  (130, 50 + yPadding)),
        manager=manager)
    OKButton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((getScreenSize() / 2 + 65 + xPadding, getScreenSize() / 2 + 25 + yPadding),
                                  (65, 50 + yPadding)),
        text='OK',
        manager=manager)
    CancelButton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((getScreenSize() / 2 + 130 + xPadding, getScreenSize() / 2 + 25 + yPadding),
                                  (65, 50 + yPadding)),
        text='Cancel',
        manager=manager)
    gameButtons = [pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0 + xPadding, getScreenSize() / 5 + 50 * i + yPadding),
                                  (getScreenSize(), 50 + yPadding)),
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
                # showing and disabling all buttons by pressing
                # also activating the functions
                if event.ui_element == CreateGameButton:
                    [button.show() for button in [CancelButton, OKButton, NameTextBox, PasswordTextBox]]
                    [button.set_text('') for button in [NameTextBox, PasswordTextBox]]
                    [button.disable() for button in [*gameButtons, CreateGameButton, RefreshButton]]
                    request = RequestType.CREATE_GAME
                # cancels the current Action
                if event.ui_element == CancelButton:
                    [button.enable() for button in [*gameButtons, CreateGameButton, RefreshButton]]
                    [button.hide() for button in [CancelButton, OKButton, NameTextBox, PasswordTextBox]]
                # commits to the action chosen
                if event.ui_element == OKButton:
                    if request == RequestType.CREATE_GAME:
                        Cardinality = Client.sendAndRecv(request, {"name": NameTextBox.get_text(), "password": PasswordTextBox.get_text()}).value

                    elif request == RequestType.JOIN_GAME:
                        print(PasswordTextBox.get_text())
                        Cardinality = Client.sendAndRecv(request, {"name": joinGameName, "password": PasswordTextBox.get_text()}).value

                    Client.sendAndRecv(RequestType.RETRIEVE_GAMES).print(True)

                    [button.kill() for button in [*gameButtons,CreateGameButton,RefreshButton,CancelButton,OKButton,NameTextBox,PasswordTextBox]]

                    hub = False
                # open game clicked
                if event.ui_element in gameButtons:
                    [button.show() for button in [CancelButton, OKButton, PasswordTextBox]]
                    [button.disable() for button in [*gameButtons, CreateGameButton, RefreshButton]]
                    PasswordTextBox.set_text('')

                    request = RequestType.JOIN_GAME
                    joinGameName = event.ui_element.text

                # refresh the buttons
                if event.ui_element == RefreshButton:
                    games = Client.sendAndRecv(RequestType.RETRIEVE_GAMES).value
                    [button.kill() for button in gameButtons]
                    gameButtons = [pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((0 + xPadding, getScreenSize() / 5 + 50 * i + yPadding),
                                                  (getScreenSize(), 50 + yPadding)),
                        text=game,
                        manager=manager) for i, game in enumerate(games)]
            manager.process_events(event)
        manager.update(timeDelta)
        manager.draw_ui(window)
        pygame.display.flip()
        window.fill((0, 0, 0))


    print(Cardinality)
    while running:
        # get the state of both games
        gameVars = Client.sendAndRecv(RequestType.GET_GAME_VARS).value
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if time.time() - delayStart > delayTime and event.button == 1:  # left click
                    delayStart = time.time()
                    # add the new ball
                    Client.send(RequestType.ADD_BALL,
                                {"x": getClampedMouse(Cardinality), "Cardinality": Cardinality,
                                 "nextFruitType": nextFruitType})
                    nextFruitType = random.choice(FruitType.fruitTypes[:4])
        keys = pygame.key.get_pressed()
        timeDelta = clock.tick(FPS) / 1000
        updateScreen(gameVars)
        
except ApplicationError as e:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
        keys = pygame.key.get_pressed()
        clock.tick(FPS)
        textBlock("ERROR SCREEN", 0.5, 0.1, 40, "white", font=pygame.font.SysFont("Arial", 40))
        textBlock(repr(e), 0.5, 0.5, 25, "white", font=pygame.font.SysFont("Arial", 25))
        pygame.display.flip()
        window.fill((255, 0, 0))
exitGame()
