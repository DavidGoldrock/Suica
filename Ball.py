import math
import FruitType
Gravity = 0.01
from pygame.draw import *


class Ball:
    def __init__(self, x: float, y, velX: float, velY: float, fruitType: FruitType):
        self.x = x
        self.y = y
        self.radius = fruitType.radius
        self.velX = velX
        self.velY = velY
        self.colFactor = 0.95
        self.fruitType = fruitType
        self.hasColided = False

    def update(self, dt: float):
        self.velY += dt * Gravity

        if self.y + self.radius + self.velY < 0.9:
            self.y += self.velY
        else:
            self.y = 0.9 - self.radius
            self.velY = 0
            self.velX *= self.colFactor

        if 0.1 <= self.x - self.radius + self.velX and self.x + self.radius + self.velX <= 0.9:
            self.x += self.velX
        else:
            self.velX *= -1


    def draw(self, window, screenSize):
        circle(window, self.fruitType.color, (self.x * screenSize[0], self.y * screenSize[1]), self.radius * screenSize[0])

    def distance(self,other):
        return math.sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))

    def collision(self, other):
        return self.distance(other) <= (self.radius + other.radius)



