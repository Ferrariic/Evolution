import math
from os import environ
from scipy.spatial import distance
from Entity.genetics import *
import string
import random

"""
    Interaction backup functions
"""
def closest_node(environment, entity):
    nodes = environment['all_entity_locations']
    node = entity.position
    nodes.remove(node)
    
    closest_node = nodes[distance.cdist([node], nodes).argmin()]
    closest_node_index = environment['all_entity_locations'].index(closest_node)
    
    x0, y0 = node
    x1, y1 = closest_node
    displacement = abs((((x0-x1)**2)+((y0-y1)**2))**(1/2))
    if displacement <= 10: # REMOVE RANGE SET 10
        interacting_with = environment['environment_json'][closest_node_index]
        return interacting_with
    return None

def update_environment(environment, entity, interaction_target):
    entity_position = environment['all_entity_names'].index(entity.name)
    environment['environment_json'][entity_position] = entity.export_entity_values()
    
    target_position = environment['all_entity_names'].index(entity.name)
    environment['environment_json'][target_position] = interaction_target

'''interaction functions'''    
# interact if within 5 coordinates of another
def interact_ATTACK(environment, entity):
    interaction_target = closest_node(environment, entity) # Finds interaction target
    # Checks to see if target can be interacted with
    if interaction_target is None:
        return
    if not interaction_target['is_Alive']: # checks to see if target is alive, can't attack a dead body lmao
        return
    if not (entity.energy > 5):
        return
    # Logic for interaction
    entity.energy -= 5
    interaction_target['health'] -= entity.strength
    if interaction_target['health'] < 0:
        interaction_target['cause_of_death'] = 'Attacked, and died.'
        entity.food += interaction_target['food'] # takes their food
        print(f"{interaction_target['name']} died fighting {entity.name}")
    
    # Update environment
    update_environment(environment, entity, interaction_target)

def interact_MATE(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if not (interaction_target['is_Alive'] & (interaction_target['can_mate'] & entity.can_mate) & (entity.is_Male != interaction_target['is_Male'])):
        return
    if not ((entity.energy > 10)&(interaction_target['energy']>10)):
        return
    
    entity.energy -= 10
    entity.children += 1
    
    interaction_target['energy'] -= 10
    interaction_target['children'] += 1
    
    '''builds child'''
    new_entity = dict()
    new_entity['name'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12))
    new_entity['food'] = random.randint(80,100)
    new_entity['children'] = 0
    new_entity['strength'] = random.randint(30,50)
    new_entity['health'] = random.randint(75,125)
    new_entity['direction'] = random.randint(0,359)
    new_entity['is_Alive'] = True
    new_entity['is_Male'] = random.choice([True, False])
    new_entity['can_mate'] = False
    new_entity['energy'] = 100
    new_entity['age'] = 0
    new_entity['brain'] = None
    new_entity['is_starving'] = False
    new_entity['job_tasks'] = 0
    new_entity['liked'] = 0
    new_entity['goal'] = None
    new_entity['inventory'] = []
    new_entity['entity_type'] = 'human'
    new_entity['genome'] =  cross_over_HEX_A_HEX(entity.genome, interaction_target['genome'])
    new_entity['position'] = random.choice([entity.position, interaction_target['position']])
    new_entity['velocity'] = random.choice([entity.velocity, interaction_target['velocity']])
    new_entity['will_Flee'] = random.choice([entity.will_Flee, interaction_target['will_Flee']])
    new_entity['generation'] = int(max([entity.generation,interaction_target['generation']])+1)
    new_entity['size'] = random.choice([entity.size, interaction_target['size']])
    new_entity['color'] = [int((entity.color[0]+interaction_target['color'][0])/2), int((entity.color[1]+interaction_target['color'][1])/2), int((entity.color[2]+interaction_target['color'][2])/2)]
    new_entity['cause_of_death'] = None
    
    update_environment(environment, entity, interaction_target) # Update parents to field
    environment['environment_json'].append(new_entity)
    print(new_entity['name'], 'child added of parents', entity.name, interaction_target['name'])
    
def interact_SHARE_FOOD(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if not interaction_target['is_Alive']:
        return
    if not ((entity.energy > 5) & (entity.food > 10)):
        return
    entity.energy -= 2
    entity.food -= 10
    entity.liked += 10
    interaction_target['food'] += 10
    update_environment(environment=environment, entity=entity, interaction_target=interaction_target)

def interact_BURY(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if interaction_target['is_Alive']:
        return
    if not (entity.energy > 5):
        return
    entity.energy -= 5

def interact_HUNT(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if not interaction_target['is_Alive']:
        return
    if not (entity.energy > 5):
        return
    entity.energy -= 5
    
def interact_HEAL_OTHER(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if not interaction_target['is_Alive']:
        return
    if not (entity.energy > 5):
        return
    entity.energy -= 5

def interact_PICK_PLANT(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if not interaction_target['is_Alive']:
        return
    if not (entity.energy > 5):
        return
    entity.energy -= 5

def interact_EAT_HUMAN(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if not (entity.energy > 5):
        return
    entity.energy -= 5