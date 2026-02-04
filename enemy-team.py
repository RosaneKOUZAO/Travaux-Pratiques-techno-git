
import Team
class EnemyTeam(Team):
    def __init__(self, unit: str, damage: int, loot: int):
        super().__init__()  # appel du constructeur de Team si nécessaire
        self.__unit = unit
        self.__damage = damage
        self.__loot = loot

    def get_damage(self):
        return self.__damage

    def get_loot(self):
        return self.__loot

    def get_unit(self):
        return self.__unit

    def __str__(self):
        return f"EnemyTeam(unit={self.__unit}, damage={self.__damage}, loot={self.__loot})"


# Test rapide
if __name__ == "__main__":
    team = EnemyTeam("Orc", 10, 5)
    print(team)
    print("Dégâts:", team.get_damage())
    print("Loot:", team.get_loot())
    print("Unit:", team.get_unit())
