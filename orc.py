import random

class Orc:
    def __init__(self):
        self.degat = random.choice([3, 4, 5])
        self.loot = random.choice([2, 2.5])

    def __str__(self):
        return f"Orc(dégat={self.degat}, loot={self.loot})"
if __name__ == "__main__":
    mon_orc = Orc()
    print(mon_orc)
