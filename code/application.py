import json
import random
from classes import*
from utility import*

class Application(object):
    def InitiateApplication(self):
        print("--- Initialisation du combat DnD ---")
        data = LoadData()
        self.aventuriers = [Warrior(data["Warrior"]), Rogue(data["Rogue"]), Mage(data["Mage"])]
        
        nb_orcs = random.randint(4, 6)
        self.horde = [Orc(data["Orc"], i+1) for i in range(nb_orcs)]
        
        print(f"L'equipe : {[a.name for a in self.aventuriers]}")
        print(f"La horde : {nb_orcs} Orcs")
        print("-" * 40)
        self.round_num = 1

    def Run(self):
        while any(a.IsAlive() for a in self.aventuriers) and any(o.IsAlive() for o in self.horde):
            print(f"\n--- ROUND {self.round_num} ---")

            all_combatants = []
            for char in self.aventuriers + self.horde:
                if char.IsAlive():
                    init_roll = RollD20()
                    all_combatants.append((init_roll, char))

            all_combatants.sort(key=lambda x: x[0], reverse=True)

            for initiative, entity in all_combatants:
                if not entity.IsAlive():
                    continue

                if isinstance(entity, Orc):
                    mes_ennemis = self.aventuriers
                    mes_amis = self.horde
                else:
                    mes_ennemis = self.horde
                    mes_amis = self.aventuriers

                if not any(e.IsAlive() for e in mes_ennemis):
                    break

                print(f"\nTour de {entity.name} (Init: {initiative})")

                entity.Special(mes_amis, mes_ennemis)

                if not any(e.IsAlive() for e in mes_ennemis):
                    break

                target = GetRandomTarget(mes_ennemis)
                if target:
                    entity.Attack(target)

            self.round_num += 1

    def TerminateApplication(self):
        print("\n" + "="*40)
        if any(a.IsAlive() for a in self.aventuriers):
            print("VICTOIRE DES AVENTURIERS !")
            survivors = [a.name for a in self.aventuriers if a.IsAlive()]
            print(f"Survivants : {', '.join(survivors)}")
        else:
            print("GAME OVER - LA HORDE A VAINCU.")