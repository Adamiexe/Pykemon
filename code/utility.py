import random
import json

def RollDice(number, value):
	res = 0
	for i in range(number):
		res += random.randint(1, value)
	return res

def RollD20():
    return random.randint(1, 20)

def LoadData():
    try:
        with open('./jsondata/bdd.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erreur: Le fichier bdd.json est introuvable.")
        exit()

def GetRandomTarget(potential_targets):
    alive_targets = [t for t in potential_targets if t.is_alive()]
    if alive_targets:
        return random.choice(alive_targets)
    return None
