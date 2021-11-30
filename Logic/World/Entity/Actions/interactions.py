import math
          
def interact_ATTACK(environment, entity):
    entity.energy -= 5
    print("attacking")

def interact_MATE(environment, entity):
    entity.energy -= 5
    print("mating")
    
def interact_SHARE_FOOD(environment, entity):
    entity.energy -= 5
    print("Sharing food")

def interact_BURY(environment, entity):
    entity.energy -= 5
    print("Burying")

def interact_HUNT(environment, entity):
    entity.energy -= 5
    print("hunting")

def interact_HEAL_OTHER(environment, entity):
    entity.energy -= 5
    print("Healing other")

def interact_PICK_PLANT(environment, entity):
    entity.energy -= 5
    print("Picking plant")

def interact_EAT_HUMAN(environment, entity):
    entity.energy -= 5
    print("Eating human")