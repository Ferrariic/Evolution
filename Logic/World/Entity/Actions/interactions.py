import math
from scipy.spatial import distance

def closest_node(environment, entity):
    nodes = environment['all_entity_locations']
    node = entity.position
    nodes.remove(node)
    
    closest_node = nodes[distance.cdist([node], nodes).argmin()]
    closest_node_index = environment['all_entity_locations'].index(closest_node)
    
    x0, y0 = node
    x1, y1 = closest_node
    displacement = abs((((x0-x1)**2)+((y0-y1)**2))**(1/2))
    if displacement <= 5:
        interacting_with = environment['environment_json'][closest_node_index]
        return interacting_with
    return None
    
# interact if within 5 coordinates of another
def interact_ATTACK(environment, entity):
    print("attacking")
    entity.energy -= 5
    interaction = closest_node(environment, entity)
    if interaction is None:
        return
    # TODO write interaction logic

def interact_MATE(environment, entity):
    entity.energy -= 5
    print("mating")
    interaction = closest_node(environment, entity)
    if interaction is None:
        return
    
def interact_SHARE_FOOD(environment, entity):
    entity.energy -= 5
    print("Sharing food")
    interaction = closest_node(environment, entity)
    if interaction is None:
        return

def interact_BURY(environment, entity):
    entity.energy -= 5
    print("Burying")
    interaction = closest_node(environment, entity)
    if interaction is None:
        return

def interact_HUNT(environment, entity):
    entity.energy -= 5
    print("hunting")
    interaction = closest_node(environment, entity)
    if interaction is None:
        return

def interact_HEAL_OTHER(environment, entity):
    entity.energy -= 5
    print("Healing other")
    interaction = closest_node(environment, entity)
    if interaction is None:
        return

def interact_PICK_PLANT(environment, entity):
    entity.energy -= 5
    print("Picking plant")
    interaction = closest_node(environment, entity)
    if interaction is None:
        return

def interact_EAT_HUMAN(environment, entity):
    entity.energy -= 5
    print("Eating human")
    interaction = closest_node(environment, entity)
    if interaction is None:
        return