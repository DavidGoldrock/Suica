import sys
import threading
import time

import pygame

from Definitions import *


class GameThread(threading.Thread):
    def __init__(self, gameVars: Game, connected: Connected, index: str):
        super().__init__(daemon=True)
        self.gameVars = gameVars
        self.connected = connected
        self.index = index


    def run(self):
        pygame.init()
        timeNow = time.time()
        clock = pygame.time.Clock()
        while self.connected.either():
            clock.tick(FPS)
            self.gameVars.player1Space.step(1 / FPS)
            self.gameVars.player2Space.step(1 / FPS)
        del games[self.index]
        sys.exit()
