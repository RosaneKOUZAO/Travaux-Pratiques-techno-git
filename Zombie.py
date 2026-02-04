import random

class Zombie:
    def __init__(self):
        # dégât aléatoire entre 1 et 2
        self.degat = random.choice([1, 2])

        # loot aléatoire entre 0.5 et 1
        self.loot = random.choice([0.5, 1])
