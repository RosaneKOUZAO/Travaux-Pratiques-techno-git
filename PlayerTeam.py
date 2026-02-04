from Team import Team

class PlayerTeam(Team):
    def __init__(
        self,
        nb_warriors: int,
        nb_hunters: int,
        nb_wizards: int,
        damage: int,
        loot: int,
        flee: int
    ):
        self.__nb_warriors = nb_warriors
        self.__nb_hunters = nb_hunters
        self.__nb_wizards = nb_wizards
        self.__damage = damage
        self.__loot = loot
        self.__flee = flee

        members = (
            ["warrior"] * nb_warriors
            + ["hunter"] * nb_hunters
            + ["wizard"] * nb_wizards
        )
        super().__init__(members)

    # ---- Méthodes d'accès ----
    def get_damage(self) -> int:
        return self.__damage

    def get_chance(self) -> int:
        return self.__nb_warriors + self.__nb_hunters + self.__nb_wizards

    def get_flee(self) -> int:
        return self.__flee

    def get_loot(self) -> int:
        return self.__loot

    def get_nb_warriors(self) -> int:
        return self.__nb_warriors

    def get_nb_hunters(self) -> int:
        return self.__nb_hunters

    def get_nb_wizards(self) -> int:
        return self.__nb_wizards

    def __repr__(self):
        return (
            "PlayerTeam("
            f"warriors={self.__nb_warriors}, "
            f"hunters={self.__nb_hunters}, "
            f"wizards={self.__nb_wizards}, "
            f"damage={self.__damage}, "
            f"loot={self.__loot}, "
            f"flee={self.__flee}"
            ")"
        )
