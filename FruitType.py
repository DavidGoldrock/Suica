class FruitType:
    def __init__(self, name:str, color: tuple[float, float, float], radius: float, nextFruitType):
        self.name = name
        self.color = color
        self.radius = radius
        self.nextFruitType = nextFruitType
    def __str__(self):
        return f"name {self.name} color {str(self.color)}, + radius {self.radius} nextFruitType: {self.nextFruitType.name}"

watermelon = FruitType("watermelon",(0, 255, 0), 0.2, None)
melon = FruitType("melon",(170, 245, 10), 0.05, watermelon)
ananas = FruitType("ananas",(222, 245, 10), 0.04, melon)
peach = FruitType("peach",(255, 145, 239), 0.03, ananas)
# lemon
# apple
# orange
# dekopon
# grape
# strawberry
# cherry
