import math


class FruitType:
    def __init__(self, index: int, name: str, color: tuple[float, float, float], radius: float, nextFruitType, points: int):
        self.index = index
        self.name = name
        self.color = color
        self.radius = radius
        self.nextFruitType = nextFruitType
        self.points = points

    def __str__(self):
        return f"name {self.name} color {str(self.color)}, + radius {self.radius} nextFruitType: {self.nextFruitType.name} index: {self.index}"


watermelon = FruitType(10, "watermelon", (0, 255, 0), 172 / 1080 * math.sqrt(2), None, 22)
melon = FruitType(9, "melon", (170, 245, 10), 160 / 1080 * math.sqrt(2), watermelon, 20)
ananas = FruitType(8, "ananas", (222, 245, 10), 144 / 1080 * math.sqrt(2), melon, 18)
peach = FruitType(7, "peach", (255, 145, 239), 128 / 1080 * math.sqrt(2), ananas, 16)
lemon = FruitType(6, "lemon", 'yellow', 112 / 1080 * math.sqrt(2), peach, 14)
apple = FruitType(5, "apple", 'red', 96 / 1080 * 2, lemon, 12)
orange = FruitType(4, "orange", 'orange', 80 / 1080 * math.sqrt(2), apple, 10)
dekopon = FruitType(3, "dekopon", (255, 40, 0), 64 / 1080 * math.sqrt(2), orange, 8)
grape = FruitType(2, "grape", 'purple', 48 / 1080 * math.sqrt(2), dekopon, 6)
strawberry = FruitType(1, "strawberry", (255, 0, 80), 32 / 1080 * math.sqrt(2), grape, 4)
cherry = FruitType(0, "cherry", 'red', 24 / 1080 * math.sqrt(2), strawberry, 2)

fruitTypes = [cherry, strawberry, grape, dekopon, orange, apple, lemon, peach, ananas, melon, watermelon]
