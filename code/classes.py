from utility import*
class Character:
    def __init__(self, stats, role_name):
        self.role = role_name
        self.name = stats.get("name", role_name)
        self.max_hp = stats["hp"]
        self.current_hp = stats["hp"]
        self.ac = stats["ac"]
        self.damage_dice = stats["damage_dice"]
        
    def IsAlive(self):
        return self.current_hp > 0

    def TakeDamage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0: self.current_hp = 0
        print(f"  > {self.name} prend {amount} degats (PV restants: {self.current_hp}/{self.max_hp})")
        if not self.IsAlive():
            print(f"   {self.name} est mort !")

    def Heal(self, amount):
        old_hp = self.current_hp
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        print(f"   {self.name} se soigne de {self.current_hp - old_hp} PV.")

    def Special(self, allies, enemies):
        
        pass

    def Attack(self, target):
        if not target or not target.IsAlive():
            return

        print(f"{self.name} attaque {target.name}...")
        roll = RollD20()

        if roll > target.ac:
            base_damage = RollDice(*self.damage_dice)
            total_damage = self.CalculateDamage(base_damage) 
            print(f"   Touche ! (Roll: {roll} vs AC: {target.ac})")
            target.TakeDamage(total_damage)
        else:
            print(f"   Loupe (Roll: {roll} vs AC: {target.ac})")
            self.OnMiss() 

    def CalculateDamage(self, base_damage):
        return base_damage

    def OnMiss(self):
        pass

class Warrior(Character):
    def __init__(self, stats):
        super().__init__(stats, "Warrior")
        self.second_wind_used = False

    def Special(self, allies, enemies):
        if not self.second_wind_used and self.current_hp < self.max_hp:
            heal_amount = RollDice(1,10)
            print(f" {self.name} utilise Second Wind !")
            self.Heal(heal_amount)
            self.second_wind_used = True

class Rogue(Character):
    def __init__(self, stats):
        super().__init__(stats, "Rogue")
        self.sneak_active = False

    def Special(self, allies, enemies):
        check = RollD20()
        if check >= 16:
            self.sneak_active = True
            print(f" {self.name} prepare une attaque sournoise ! (Check: {check} >= 16)")
        else:
            self.sneak_active = False
            print(f"{self.name} rate sa preparation sournoise. (Check: {check})")

    def CalculateDamage(self, base_damage):
        if self.sneak_active:
            bonus = RollDice(4,6)
            print(f"   CRITIQUE SOURNOIS ! (+{bonus} degats)")
            self.sneak_active = False
            return base_damage + bonus
        return base_damage
    
    def OnMiss(self):
        self.sneak_active = False

class Mage(Character):
    def __init__(self, stats):
        super().__init__(stats, "Mage")

    def Special(self, allies, enemies):
        check = RollD20()
        if check >= 18:
            print(f" {self.name} canalise une BOULE DE FEU ! (Check: {check} >= 18)")
            damage = RollDice(4,10)
            print(f"   La boule de feu explose pour {damage} degats sur TOUS les ennemis !")
            for enemy in enemies:
                if enemy.IsAlive():
                    enemy.TakeDamage(damage)

class Orc(Character):
    def __init__(self, stats, number):
        super().__init__(stats, "Orc")
        self.name = f"Orc #{number}"
