import math
import FruitType
from pygame.draw import *
import pymunk


class Ball:
    def __init__(self, x: float, y, fruitType: FruitType):
        self.fruitType = fruitType
        self.body, self.shape = self.getObject(x, y, fruitType.radius)
        self.colFactor = 0.992
        self.hasColided = False

    def getObject(self, x, y, radius):
        body = pymunk.Body(radius, pymunk.moment_for_circle(radius, 0, radius), body_type=pymunk.Body.DYNAMIC)
        body.position = (x, y)
        shape = pymunk.Circle(body, radius)
        shape.mass = radius
        shape.collision_type = FruitType.fruitTypes.index(self.fruitType)
        return body, shape

    def addObject(self, space):
        space.add(self.body, self.shape)

    @staticmethod
    def drawBall(x, y, fruitType, window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize):
        circle(window, fruitType.color, (ZERO_X + x * (ONE_X - ZERO_X), ZERO_Y + y * (ONE_Y - ZERO_Y)),
               fruitType.radius * (ONE_X - ZERO_X))

    def draw(self, window, ZERO_X, ONE_X, ZERO_Y, ONE_Y, screenSize):
        Ball.drawBall(self.body.position.x, self.body.position.y, self.fruitType, window, ZERO_X, ONE_X, ZERO_Y, ONE_Y,
                      screenSize)
