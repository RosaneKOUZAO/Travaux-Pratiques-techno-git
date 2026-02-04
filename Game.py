import json
import os
import random
from typing import Any, Dict, Optional

from PlayerTeam import PlayerTeam
from EnemyTeam import EnemyTeam


class Game:
    # attribut de classe
    history_file = "game_history.json"

    def __init__(self):
        # attribut privé
        self.__game_status: Optional[Dict[str, Any]] = None

    # -------------------------
    # I/O fichier texte (JSON)
    # -------------------------
    def __read_file(self) -> Dict[str, Any]:
        if not os.path.exists(self.history_file):
            return {}
        with open(self.history_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}

    def __write_file(self, data: Dict[str, Any]) -> None:
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # -------------------------
    # Méthodes demandées
    # -------------------------
    def config(self) -> None:
        """
        Configure la partie et sauvegarde dans le fichier texte.
        Demande le nom du joueur et initialise l'état.
        """
        name = input("Nom du joueur : ").strip()
        if not name:
            name = "Joueur"

        data = {
            "player_name": name,
            "context": "mouvement",
            "loot": 40.0,
            "game_over": False,

            # Team joueur (compteurs)
            "player_team": {"warrior": 0, "hunter": 0, "wizard": 0},

            # Stats de l'équipe joueur (stockées car PlayerTeam les attend)
            "player_stats": {"damage": 0, "loot": 0, "flee": 1},

            # Team ennemie (None si pas en combat)
            "enemy_team": None,  # ex: {"warrior":1,"hunter":0,"wizard":2}
            "enemy_stats": None,  # ex: {"damage":8,"loot":10,"flee":3}
        }

        self.__write_file(data)
        self.load_game()

    def status(self) -> None:
        """
        Affiche l'état courant de la partie.
        """
        self.load_game()
        data = self.__game_status
        if not data:
            print("Aucune partie trouvée. Lance config.")
            return

        if data.get("game_over"):
            print("GAME OVER")
            return

        team = data.get("player_team", {})
        w = int(team.get("warrior", 0))
        h = int(team.get("hunter", 0))
        m = int(team.get("wizard", 0))

        print(f"Joueur : {data.get('player_name', '')}")
        print(f"Butin : {data.get('loot', 40.0)}")
        print(f"Équipe : warriors={w}, hunters={h}, wizards={m}")
        print(f"Contexte : {data.get('context', 'mouvement')}")

        if data.get("context") == "mouvement":
            print("Actions possibles : buy <warrior|hunter|wizard> | move <north|south|east|west> | status")
        else:
            print("Actions possibles : fight | flee | status")

    def __load_player_team(self) -> PlayerTeam:
        """
        Retourne une instance de PlayerTeam à partir du fichier texte.
        """
        data = self.__read_file()
        team = data.get("player_team", {"warrior": 0, "hunter": 0, "wizard": 0})
        stats = data.get("player_stats", {"damage": 0, "loot": 0, "flee": 1})

        return PlayerTeam(
            nb_warriors=int(team.get("warrior", 0)),
            nb_hunters=int(team.get("hunter", 0)),
            nb_wizards=int(team.get("wizard", 0)),
            damage=int(stats.get("damage", 0)),
            loot=int(stats.get("loot", 0)),
            flee=int(stats.get("flee", 1)),
        )

    def __load_enemy_team(self) -> Optional[EnemyTeam]:
        """
        Retourne une instance de EnemyTeam à partir du fichier texte.
        """
        data = self.__read_file()
        team = data.get("enemy_team")
        stats = data.get("enemy_stats")
        if not team or not stats:
            return None

        return EnemyTeam(
            nb_warriors=int(team.get("warrior", 0)),
            nb_hunters=int(team.get("hunter", 0)),
            nb_wizards=int(team.get("wizard", 0)),
            damage=int(stats.get("damage", 0)),
            loot=int(stats.get("loot", 0)),
            flee=int(stats.get("flee", 1)),
        )

    def player_damage(self) -> int:
        """
        Retourne la somme des dégâts des unités de l'équipe du joueur.
        Ici : on renvoie la valeur damage stockée dans PlayerTeam.
        (tu peux aussi recalculer si ton TD le demande plus tard)
        """
        team = self.__load_player_team()
        return team.get_damage()

    def enemy_damage(self) -> int:
        """
        Retourne la somme des dégâts des unités de l'équipe ennemie.
        """
        enemy = self.__load_enemy_team()
        return enemy.get_damage() if enemy else 0

    def load_game(self) -> None:
        """
        Charge l'état de la partie à partir du fichier texte.
        """
        self.__game_status = self.__read_file() or None

    def start_game(self) -> None:
        """
        Redémarre la partie en écrasant les données du fichier texte.
        Le nom du joueur est conservé.
        """
        data = self.__read_file()
        name = data.get("player_name", "Joueur")

        new_data = {
            "player_name": name,
            "context": "mouvement",
            "loot": 40.0,
            "game_over": False,
            "player_team": {"warrior": 0, "hunter": 0, "wizard": 0},
            "player_stats": {"damage": 0, "loot": 0, "flee": 1},
            "enemy_team": None,
            "enemy_stats": None,
        }
        self.__write_file(new_data)
        self.load_game()

    def buy(self, unit: str) -> None:
        """
        Achète l'unité choisie et met à jour le fichier texte.
        Achat uniquement hors combat.
        """
        unit = unit.lower().strip()
        if unit not in ("warrior", "hunter", "wizard"):
            print("Unité inconnue : warrior | hunter | wizard")
            return

        data = self.__read_file()
        if not data:
            print("Aucune partie. Lance config.")
            return
        if data.get("game_over"):
            print("GAME OVER")
            return
        if data.get("context") != "mouvement":
            print("Achat impossible en combat.")
            return

        # Prix simples (à adapter si votre TD impose d'autres prix)
        PRICE = {"warrior": 10.0, "hunter": 8.0, "wizard": 12.0}
        loot = float(data.get("loot", 40.0))

        if loot < PRICE[unit]:
            print("Butin insuffisant.")
            return

        loot -= PRICE[unit]
        data["loot"] = loot

        data.setdefault("player_team", {"warrior": 0, "hunter": 0, "wizard": 0})
        data["player_team"][unit] = int(data["player_team"].get(unit, 0)) + 1

        # Mise à jour des stats équipe joueur (damage, flee, loot interne d'équipe)
        # Ici : modèle simple (à ajuster si vous avez des stats par unité)
        DAMAGE_PER = {"warrior": 3, "hunter": 2, "wizard": 4}
        FLEE_PER = {"warrior": 2, "hunter": 4, "wizard": 3}

        stats = data.get("player_stats", {"damage": 0, "loot": 0, "flee": 1})
        stats["damage"] = int(stats.get("damage", 0)) + DAMAGE_PER[unit]
        stats["flee"] = int(stats.get("flee", 1)) + FLEE_PER[unit]
        data["player_stats"] = stats

        self.__write_file(data)
        self.load_game()

    def move(self, direction: str) -> None:
        """
        Charge le fichier texte et calcule le résultat du mouvement cf README
        puis met à jour le fichier texte.
        """
        direction = direction.lower().strip()
        if direction not in ("north", "south", "east", "west", "n", "s", "e", "w"):
            print("Direction invalide : north/south/east/west")
            return

        data = self.__read_file()
        if not data:
            print("Aucune partie. Lance config.")
            return
        if data.get("game_over"):
            print("GAME OVER")
            return
        if data.get("context") != "mouvement":
            print("Déplacement impossible en combat.")
            return

        player_team = self.__load_player_team()
        chance = player_team.get_chance()

        p_loot = min(0.2, (chance / 5) / 100)
        p_soldiers = min(0.1, (chance / 10) / 100)
        p_enemy = min(0.2, (chance / 4) / 100)

        r = random.random()
        t1 = p_loot
        t2 = t1 + p_soldiers
        t3 = t2 + p_enemy

        if r < t1:
            found = random.choice([5, 10, 15])
            data["loot"] = float(data.get("loot", 40.0)) + found
            data["context"] = "mouvement"
            data["enemy_team"] = None
            data["enemy_stats"] = None
            print(f"Découverte d'un butin : +{found}")

        elif r < t2:
            # Soldats errants (modèle simple : +1 warrior)
            data.setdefault("player_team", {"warrior": 0, "hunter": 0, "wizard": 0})
            data["player_team"]["warrior"] = int(data["player_team"].get("warrior", 0)) + 1

            # impact sur stats joueur
            stats = data.get("player_stats", {"damage": 0, "loot": 0, "flee": 1})
            stats["damage"] = int(stats.get("damage", 0)) + 3
            stats["flee"] = int(stats.get("flee", 1)) + 2
            data["player_stats"] = stats

            data["context"] = "mouvement"
            data["enemy_team"] = None
            data["enemy_stats"] = None
            print("Découverte de soldats errants : +1 warrior")

        elif r < t3:
            # Équipe ennemie aléatoire (simple)
            ew = random.choice([0, 1, 2])
            eh = random.choice([0, 1, 2])
            em = random.choice([0, 1, 2])

            enemy_damage = ew * 3 + eh * 2 + em * 4
            enemy_loot = random.choice([5, 10, 15])
            enemy_flee = max(1, random.choice([1, 2, 3, 4]))

            data["enemy_team"] = {"warrior": ew, "hunter": eh, "wizard": em}
            data["enemy_stats"] = {"damage": enemy_damage, "loot": enemy_loot, "flee": enemy_flee}
            data["context"] = "combat"

            print("Découverte d'une équipe ennemie : contexte COMBAT")

        else:
            # Lieu sûr
            data["context"] = "mouvement"
            data["enemy_team"] = None
            data["enemy_stats"] = None
            print("Lieu sûr : rien ne se passe")

        self.__write_file(data)
        self.load_game()

    def fight(self) -> None:
        """
        Charge le fichier texte, simule le combat et met à jour le fichier texte.
        """
        data = self.__read_file()
        if not data:
            print("Aucune partie. Lance config.")
            return
        if data.get("game_over"):
            print("GAME OVER")
            return
        if data.get("context") != "combat":
            print("Pas de combat en cours.")
            return
        if not data.get("enemy_team") or not data.get("enemy_stats"):
            print("Aucun ennemi chargé.")
            return

        player_team = self.__load_player_team()
        enemy_team = self.__load_enemy_team()

        player_dmg = player_team.get_damage()
        enemy_dmg = enemy_team.get_damage() if enemy_team else 0

        if player_dmg > enemy_dmg:
            gain = float(data["enemy_stats"].get("loot", 0))
            data["loot"] = float(data.get("loot", 40.0)) + gain
            data["context"] = "mouvement"
            data["enemy_team"] = None
            data["enemy_stats"] = None
            print(f"Victoire ! +{gain} butin")
        else:
            data["game_over"] = True
            print("Défaite... GAME OVER")

        self.__write_file(data)
        self.load_game()

    def flee(self) -> None:
        """
        Charge le fichier texte, simule la fuite et met à jour le fichier texte.
        Lors d'une fuite, chaque unité peut mourir.
        chance de mourir d'une unité : 1 / score de fuite
        """
        data = self.__read_file()
        if not data:
            print("Aucune partie. Lance config.")
            return
        if data.get("game_over"):
            print("GAME OVER")
            return
        if data.get("context") != "combat":
            print("Pas en combat : fuite impossible.")
            return
        if not data.get("enemy_stats"):
            print("Aucun ennemi chargé.")
            return

        flee_score = int(data["enemy_stats"].get("flee", 1))
        flee_score = max(1, flee_score)
        p_die = 1.0 / flee_score

        team = data.get("player_team", {"warrior": 0, "hunter": 0, "wizard": 0})

        def survivors(count: int) -> int:
            alive = 0
            for _ in range(int(count)):
                if random.random() >= p_die:
                    alive += 1
            return alive

        new_w = survivors(int(team.get("warrior", 0)))
        new_h = survivors(int(team.get("hunter", 0)))
        new_m = survivors(int(team.get("wizard", 0)))

        team["warrior"] = new_w
        team["hunter"] = new_h
        team["wizard"] = new_m
        data["player_team"] = team

        # Recalcule stats joueur selon le modèle simple
        DAMAGE_PER = {"warrior": 3, "hunter": 2, "wizard": 4}
        FLEE_PER = {"warrior": 2, "hunter": 4, "wizard": 3}

        stats = data.get("player_stats", {"damage": 0, "loot": 0, "flee": 1})
        stats["damage"] = new_w * DAMAGE_PER["warrior"] + new_h * DAMAGE_PER["hunter"] + new_m * DAMAGE_PER["wizard"]
        stats["flee"] = 1 + new_w * FLEE_PER["warrior"] + new_h * FLEE_PER["hunter"] + new_m * FLEE_PER["wizard"]
        data["player_stats"] = stats

        # fin du combat
        data["context"] = "mouvement"
        data["enemy_team"] = None
        data["enemy_stats"] = None

        print("Fuite effectuée. Certaines unités ont peut-être péri.")

        self.__write_file(data)
        self.load_game()
