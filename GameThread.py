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

        while self.connected.either():
            pass
        del games[self.index]
        sys.exit()
