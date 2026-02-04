import random


class Gobelin:
    def __init__(self):
        # dégât aléatoire entre 2 et 3
        self.degat = random.choice([2, 3])

        # loot aléatoire entre 1 et 1.5
        self.loot = random.choice([1, 1.5])