class FruitType:
    def __init__(self, name: str, color: tuple[float, float, float], radius: float, nextFruitType):
        self.name = name
        self.color = color
        self.radius = radius
        self.nextFruitType = nextFruitType

    def __str__(self):
        return f"name {self.name} color {str(self.color)}, + radius {self.radius} nextFruitType: {self.nextFruitType.name}"


watermelon = FruitType("watermelon", (0, 255, 0), 172 / 1080, None)
melon = FruitType("melon", (170, 245, 10), 160 / 1080, watermelon)
ananas = FruitType("ananas", (222, 245, 10), 144 / 1080, melon)
peach = FruitType("peach", (255, 145, 239), 128 / 1080, ananas)
lemon = FruitType("lemon", 'yellow', 112 / 1080, peach)
apple = FruitType("apple", 'red', 96 / 1080, lemon)
orange = FruitType("orange", 'orange', 80 / 1080, apple)
dekopon = FruitType("dekopon", (255,40,0), 64 / 1080, orange)
grape = FruitType("grape", 'purple', 48 / 1080, dekopon)
strawberry = FruitType("strawberry", (255,0,80), 32 / 1080, grape)
cherry = FruitType("cherry", 'red', 24 / 1080, strawberry)

fruitTypes = [cherry, strawberry, grape, dekopon, orange, apple, lemon, peach, ananas, melon, watermelon]

