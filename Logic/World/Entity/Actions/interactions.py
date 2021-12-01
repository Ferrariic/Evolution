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
    
    # Update environment
    update_environment(environment, entity, interaction_target)

def interact_MATE(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if not (interaction_target['is_Alive'] & (interaction_target['can_mate'] & entity.can_mate) & (entity.is_Male != interaction_target['is_Male'])):
        return
    if not ((entity.energy > 10) & (interaction_target['energy']>10)):
        return
    
    entity.energy -= 10
    entity.children += 1
    
    interaction_target['energy'] -= 10
    interaction_target['children'] += 1
    
    '''builds child'''
    new_entity = mate_parents_OBJ_DICT(entity=entity, interaction_target=interaction_target)
    update_environment(environment, entity, interaction_target) # Update parents to field
    environment['environment_json'].append(new_entity)
    
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
    entity.food -= 2
    interaction_target['health'] += 20
    update_environment(environment=environment, entity=entity, interaction_target=interaction_target)

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