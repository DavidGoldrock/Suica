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
    print(data)
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


def setupSpace(balls: List[Ball]) -> pymunk.Space:
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
        handler.begin = (lambda arbiter, space, data, i=i: handleCollision(arbiter, space, i))
    return space


class Game:
    def __init__(self):

        self.player1Score = 0
        self.player2Score = 0
        self.player1X = 0.5
        self.player2X = 0.5
        self.player1Balls = []
        self.player2Balls = []
        self.player1Space = setupSpace(self.player1Balls)
        self.player2Space = setupSpace(self.player2Balls)

    def generateNewFruit(self, x, Cardinality, nextFruitType: FruitType):
        if Cardinality == 0:
            space = self.player1Space
            self.player1Score += nextFruitType.points
        elif Cardinality == 1:
            space = self.player2Space
            self.player1Score += nextFruitType.points
        nextFruit = Ball(x, 0, nextFruitType)
        nextFruit.addObject(space)
        if Cardinality == 0:
            self.player1Balls.append(nextFruit)
        elif Cardinality == 1:
            self.player2Balls.append(nextFruit)

    def toByteArray(self):
        dilld_space1 = dill.dumps(self.player1Space)
        return struct.pack('d', self.player1X) + \
            struct.pack('d', self.player2X) + \
            self.player1Score.to_bytes(4, 'little') + \
            self.player2Score.to_bytes(4, 'little') + \
            len(dilld_space1).to_bytes(4, 'little') + \
            dilld_space1 + \
            len(dill.dumps(self.player2Space)).to_bytes(4, 'little') + \
            dill.dumps(self.player2Space) + \
            len(dill.dumps(self.player1Balls)).to_bytes(4, 'little') + \
            dill.dumps(self.player1Balls) + \
            len(dill.dumps(self.player2Balls)).to_bytes(4, 'little') + \
            dill.dumps(self.player2Balls)

    @staticmethod
    def fromByteArray(arr: bytearray):
        g = Game()
        g.player1y = struct.unpack('d', arr[0:8])[0]
        g.player2y = struct.unpack('d', arr[8:16])[0]
        g.player1Score = int.from_bytes(arr[16:20], 'little')
        g.player2Score = int.from_bytes(arr[20:24], 'little')
        player1SpaceLength = int.from_bytes(arr[24:28], 'little')
        g.player1Space = dill.loads(arr[28:28 + player1SpaceLength])
        player2SpaceLength = int.from_bytes(arr[28 + player1SpaceLength:28 + player1SpaceLength + 4], 'little')
        g.player2Space = dill.loads(arr[28 + player1SpaceLength + 4:28 + player1SpaceLength + 4 + player2SpaceLength])
        player1BallsLength = int.from_bytes(
            arr[28 + player1SpaceLength + 4 + player2SpaceLength:28 + player1SpaceLength + 4 + player2SpaceLength + 4],
            'little')
        g.player1Balls = dill.loads(arr[
                                    28 + player1SpaceLength + 4 + player2SpaceLength + 4:28 + player1SpaceLength + 4 + player2SpaceLength + 4 + player1BallsLength])
        player2BallsLength = int.from_bytes(
            arr[
            28 + player1SpaceLength + 4 + player2SpaceLength + 4 + player1BallsLength:28 + player1SpaceLength + 4 + player2SpaceLength + 4 + player1BallsLength + 4],
            'little')
        g.player1Balls = dill.loads(arr[
                                    28 + player1SpaceLength + 4 + player2SpaceLength + 4 + player1BallsLength + 4:28 + player1SpaceLength + 4 + player2SpaceLength + 4 + player1BallsLength + 4 + player2BallsLength])

        return g


def randStr(N: int, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(N))
