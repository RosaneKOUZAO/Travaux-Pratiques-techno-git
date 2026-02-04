import random

class Wizard:
    def __init__(self):
        self.degat = random.choice([2, 3, 4])
        self.chance = 20
        self.fuite = 10
        self.prix = 15
        self.type_unite = "wizard"

    def __str__(self):
        return f"Wizard(degat={self.degat}, chance={self.chance}, fuite={self.fuite}, prix={self.prix})"

# Test simple
if __name__ == "__main__":
    w = Wizard()
    print(w)
