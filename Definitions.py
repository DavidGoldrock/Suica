from __future__ import annotations
import math
import struct
import random
import string

PORT = 5050
HEADER = 4
FORMAT = 'utf-8'
DISTANCE_FROM_WALL = 0.1
BALL_WIDTH = 0.02
PLAYER_HEIGHT = 0.15
PLAYER_WIDTH = 0.025
FPS = 60
Gravity = 0.7
screenPercents = (700 / 1080, 700 / 1080)
games = {}


class Connected:
    def __init__(self, connected1, connected2):
        self.connected1 = connected1
        self.connected2 = connected2
        self.gameOn = False

    def either(self):
        return self.connected1 or self.connected2

    def Both(self):
        return self.connected1 and self.connected2

    def xor(self):
        return self.connected1 != self.connected2

    def nor(self):
        return not (self.connected1 or self.connected2)

    def __str__(self):
        return f"1: {self.connected1} 2: {self.connected2}"


class Game:
    def __init__(self):
        pass

    def toByteArray(self):
        return bytearray()

    @staticmethod
    def fromByteArray(arr: bytearray):
        g = Game()
        return g


def randStr(N: int, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(N))
