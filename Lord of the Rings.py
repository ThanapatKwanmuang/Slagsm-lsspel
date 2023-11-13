import random

class Weapon:
    def __init__(self, name, damage_range, element):
        self.name = name
        self.damage_range = damage_range
        self.element = element

    def attack(self, xp, level):
        base_damage = random.randint(self.damage_range[0], self.damage_range[1])
        bonus_damage = int((xp + level) / 10)
        total_damage = base_damage + bonus_damage
        return total_damage

class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

class Fighter:
    fighters_names = set()

    def __init__(self, name=None):
        if name is None:
            self.name = self.generate_random_name()
        else:
            self.name = name
            self.fighters_names.add(name)

        self.health = 100
        self.max_mana = 50
        self.mana = self.max_mana
        self.weapon = None
        self.armor = None
        self.xp = 0
        self.level = 1

    def generate_random_name(self):
        names = ["Aragor", "Legalos", "Gibli", "Frobo", "Gendalf", "Souron", "Sarumon", "Biromir"]
        available_names = set(names) - self.fighters_names
        return random.choice(list(available_names))

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def attack(self, opponent):
        damage = self.weapon.attack(self.xp, self.level)
        element_multiplier = 1.5 if self.weapon.element == "Fire" and opponent.armor and opponent.armor.name == "IceArmor" else 1.0
        total_damage = int(damage * element_multiplier) - (opponent.armor.defense if opponent.armor else 0)
        opponent.take_damage(max(0, total_damage))
        print(f"{self.name} attacks {opponent.name} with {self.weapon.name} for {total_damage} damage.")

        self.xp += total_damage // 2

    def defend(self):
        print(f"{self.name} defends and gains 10 mana.")
        self.mana = min(self.max_mana, self.mana + 10)

    def heal(self):
        if self.mana >= 20:
            print(f"{self.name} heals and spends 20 mana.")
            self.health = min(100, self.health + 20)
            self.mana -= 20
        else:
            print(f"{self.name} does not have enough mana to heal.")

    def display_status(self):
        print(f"{self.name}: Health = {self.health}, Mana = {self.mana}, Level = {self.level}, XP = {self.xp}")

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.health += 10
        self.mana = min(self.max_mana, self.mana + 10)
        self.weapon.damage_range = (self.weapon.damage_range[0] + 5, self.weapon.damage_range[1] + 5)

class Arena:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2

    def run_fight(self):
        print("Fight starts!")
        while self.fighter1.is_alive() and self.fighter2.is_alive():
            print("\nOptions:")
            print("1. Attack")
            print("2. Defend")
            print("3. Heal")

            choice = input("Choose an option: ")

            if choice == "1":
                self.fighter1.attack(self.fighter2)
            elif choice == "2":
                self.fighter1.defend()
            elif choice == "3":
                self.fighter1.heal()
            else:
                print("Invalid option. Please choose again.")
                continue

            self.fighter2.display_status()

            if not self.fighter2.is_alive():
                print(f"{self.fighter2.name} has been defeated!")
                break

            self.fighter2.attack(self.fighter1)
            self.fighter1.display_status()

            if not self.fighter1.is_alive():
                print(f"{self.fighter1.name} has been defeated!")

            self.fighter2.xp += (self.fighter1.weapon.attack(self.fighter1.xp, self.fighter1.level) // 2)

            if self.fighter1.xp >= 50:
                self.fighter1.level_up()

            if self.fighter2.xp >= 50:
                self.fighter2.level_up()

if __name__ == "__main__":
    fighters = []

    player_choice = input("Choose player control (1 - Player, 2 - Computer, 3 - PvP): ")

    fighter1 = Fighter()
    fighters.append(fighter1)

    fighter2 = Fighter()
    fighters.append(fighter2)

    if player_choice == "1":
        fighter1.weapon = Weapon("Excalibur", (5, 15), "Normal")
        fighter1.armor = Armor("SteelArmor", 5)
    else:
        fighter1.weapon = Weapon("Excalibur", (5, 15), "Normal")
        fighter1.armor = Armor("SteelArmor", 5)

    fighter2.weapon = Weapon("Zenith", (8, 18), "Fire")
    fighter2.armor = Armor("IceArmor", 3)

    arena = Arena(fighter1, fighter2)
    arena.run_fight()

