import math
import FruitType
from pygame.draw import *
from Defenitions import *
import pymunk


class Ball:
    def __init__(self, x: float, y, position, fruitType: FruitType):
        self.fruitType = fruitType
        self.body, self.shape = self.getObject(x, y, fruitType.radius)
        self.position = position
        self.colFactor = 0.992
        self.hasColided = False
    def getObject(self, x, y, radius):
        body = pymunk.Body(radius, pymunk.moment_for_circle(radius,0,radius), body_type=pymunk.Body.DYNAMIC)
        body.position = (x, y)
        shape = pymunk.Circle(body, radius)
        shape.mass = radius
        shape.collision_type = FruitType.fruitTypes.index(self.fruitType)
        return body, shape

    def addObject(self, space):
        space.add(self.body, self.shape)


    def draw(self, window, screenSize, xPadding, yPadding):
        x,y = self.body.position
        circle(window, self.fruitType.color, (xPadding + self.body.position.x * screenSize, yPadding + self.body.position.y * screenSize),
               self.shape.radius * screenSize)
