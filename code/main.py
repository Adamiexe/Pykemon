import json

from classes import Warrior, Rogue, Mage, Orc
from utility import*

def main():
    print("--- Initialisation du combat DnD ---")
    data = LoadData()

    aventuriers = [Warrior(data["Warrior"]),Rogue(data["Rogue"]),Mage(data["Mage"])]
    
    nb_orcs = random.randint(4, 6)
    horde = [Orc(data["Orc"], i+1) for i in range(nb_orcs)]
    
    print(f"L'equipe : {[a.name for a in aventuriers]}")
    print(f"La horde : {nb_orcs} Orcs")
    print("-" * 40)

    round_num = 1

    while any(a.is_alive() for a in aventuriers) and any(o.is_alive() for o in horde):
        print(f"\n--- ROUND {round_num} ---")

        all_combatants = []
        for char in aventuriers + horde:
            if char.is_alive():
                init_roll = RollD20()
                all_combatants.append((init_roll, char))

        all_combatants.sort(key=lambda x: x[0], reverse=True)

        for initiative, entity in all_combatants:
            if not entity.is_alive():
                continue

            if isinstance(entity, Orc):
                mes_ennemis = aventuriers
                mes_amis = horde
            else:
                mes_ennemis = horde
                mes_amis = aventuriers

            if not any(e.is_alive() for e in mes_ennemis):
                break

            print(f"\nTour de {entity.name} (Init: {initiative})")

            entity.special(mes_amis, mes_ennemis)

            if not any(e.is_alive() for e in mes_ennemis):
                break

            target = GetRandomTarget(mes_ennemis)
            if target:
                entity.attack(target)
        
        round_num += 1

    print("\n" + "="*40)
    if any(a.is_alive() for a in aventuriers):
        print("VICTOIRE DES AVENTURIERS !")
        survivors = [a.name for a in aventuriers if a.is_alive()]
        print(f"Survivants : {', '.join(survivors)}")
    else:
        print("GAME OVER - LA HORDE A VAINCU.")

if __name__ == "__main__":
    main()