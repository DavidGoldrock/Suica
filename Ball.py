import math
import FruitType
from pygame.draw import *
from Defenitions import *

class Ball:
    def __init__(self, x: float, y, velX: float, velY: float, fruitType: FruitType):
        self.x = x
        self.y = y
        self.radius = fruitType.radius
        self.velX = velX
        self.velY = velY
        self.colFactor = 0.992
        self.fruitType = fruitType
        self.hasColided = False

    def update(self, dt: float):
        self.velY += dt * Gravity

        if self.y + self.radius + self.velY < 0.5 + screenPercents[1] / 2:
            self.y += self.velY
        else:
            self.y = 0.5 + screenPercents[1] / 2 - self.radius
            self.velY = 0
            self.velX *= self.colFactor

        if 0.5 - screenPercents[0] / 2 <= self.x - self.radius + self.velX and self.x + self.radius + self.velX <= 0.5 + screenPercents[0] / 2:
            self.x += self.velX
        else:
            self.velX *= -1
            self.x = max(min(self.x, 0.5 + screenPercents[0] / 2 - self.radius), 0.5 - screenPercents[0] / 2 + self.radius)



    def draw(self, window, screenSize, xPadding, yPadding):
        circle(window, self.fruitType.color, (xPadding + self.x * screenSize, yPadding + self.y * screenSize), self.radius * screenSize)

    def distance(self,other):
        return math.sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))

    def collision(self, other):
        return self.distance(other) <= (self.radius + other.radius)

    def intersections(self,other):
        x0 = self.x
        y0 = self.y
        x1 = other.x
        y1 = other.y
        r0 = self.radius
        r1 = other.radius
        d = math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
        a = (r0 * r0 - r1 * r1 + d * d) / (2 * d)
        h = math.sqrt(r0 * r0 - a * a)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d
        return (x3,y3), (x2,y2)



