from __future__ import annotations
import struct
import random
import string
import pymunk
from Ball import Ball
from typing import List
import dill
import dill

import FruitType

PORT = 5050
HEADER = 8
FORMAT = 'utf-8'
DISTANCE_FROM_WALL = 0.1
BALL_WIDTH = 0.02
PLAYER_HEIGHT = 0.15
PLAYER_WIDTH = 0.025
FPS = 60
Gravity = 0.7
screenPercents = (700 / 1080, 700 / 1080)
games = {}


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


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


def handleCollision(arbiter, space, data, balls: List[Ball], addPoints):
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
    colidedBall = Ball(newX, newY, FruitType.fruitTypes[data + 1])
    addPoints(colidedBall.fruitType.points)
    colidedBall.addObject(space)
    balls.append(colidedBall)

    return True


def setupSpace(balls: List[Ball], addPoints) -> pymunk.Space:
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
    for i in range(len(FruitType.fruitTypes)):
        handler = space.add_collision_handler(i, i)
        handler.begin = (lambda arbiter, space, data, i=i: handleCollision(arbiter, space, i, balls, addPoints))
    return space


class Game:
    def __init__(self):

        self.player1Score = 0
        self.player2Score = 0
        self.player1X = 0.5
        self.player2X = 0.5
        self.player1Balls = []
        self.player2Balls = []

        def addPoints1(points):
            self.player1Score += points

        def addPoints2(points):
            self.player2Score += points

        self.player1Space = setupSpace(self.player1Balls, addPoints1)
        self.player2Space = setupSpace(self.player2Balls, addPoints2)

    def generateNewFruit(self, x, Cardinality, nextFruitType: FruitType):
        space = None
        if Cardinality == 0:
            space = self.player1Space
            self.player1Score += nextFruitType.points
        elif Cardinality == 1:
            space = self.player2Space
            self.player1Score += nextFruitType.points
        print(space)
        nextFruit = Ball(x, 0, nextFruitType)
        nextFruit.addObject(space)
        if Cardinality == 0:
            self.player1Balls.append(nextFruit)
        elif Cardinality == 1:
            self.player2Balls.append(nextFruit)

    def toByteArray(self):
        return dill.dumps(
            [
                self.player1X,
                self.player2X,
                self.player1Score,
                self.player2Score,
                self.player1Space,
                self.player2Space,
                self.player1Balls,
                self.player2Balls,

            ]
        )

    @staticmethod
    def fromByteArray(arr: bytearray):
        g = Game()
        arr = dill.loads(arr)
        g.player1X = arr[0]
        g.player2X = arr[1]
        g.player1Score = arr[2]
        g.player2Score = arr[3]
        g.player1Space = arr[4]
        g.player2Space = arr[5]
        g.player1Balls = arr[6]
        g.player2Balls = arr[7]
        return g

    def __str__(self):
        return f"player1X {self.player1X} player2X {self.player2X} player1Score {self.player1Score} player2Score {self.player2Score} player1Space {self.player1Space} player2Space {self.player2Space} player1Balls {self.player1Balls} player2Balls {self.player2Balls}"


def randStr(N: int, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(N))
