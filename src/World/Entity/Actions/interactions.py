from os import environ
from scipy.spatial import distance
from Entity.genetics import *

"""
    Interaction backup functions
"""
def closest_node(environment, entity, distance_threshold=16):
    nodes = environment['all_entity_locations'][:]
    node = entity.position
    
    nodes.remove(node)
    
    closest_node = nodes[distance.cdist([node], nodes).argmin()]
    closest_node_index = environment['all_entity_locations'].index(closest_node)
    
    x0, y0 = node
    x1, y1 = closest_node
    displacement = abs((((x0-x1)**2)+((y0-y1)**2))**(1/2))
    if displacement <= distance_threshold:
        interacting_with = environment['environment_json'][closest_node_index]
        if interacting_with['name'] == entity.name:
            return None
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
    environment['attack_interactions'] = environment['attack_interactions'] + [entity.position, interaction_target['position']]
    entity.energy -= 5
    interaction_target['health'] -= entity.strength*entity.size
    print(f"{entity.name} -ATTACKED-> {interaction_target['name']}")
    if interaction_target['health'] < 0:
        print(f"{entity.name} -KILLED-> {interaction_target['name']}")
        interaction_target['cause_of_death'] = 'Attacked'
        entity.food += (interaction_target['food'] + interaction_target['health']*interaction_target['size']) # takes their food
    
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
    
    environment['mate_interactions'] = environment['mate_interactions'] + [entity.position, interaction_target['position']]
    entity.energy -= 10
    entity.children += 1
    
    interaction_target['energy'] -= 10
    interaction_target['children'] += 1
    
    '''builds child'''
    new_entity = mate_parents_OBJ_DICT(entity=entity, interaction_target=interaction_target)
    
    child_name = new_entity['name']
    parent_name = interaction_target['name']
    print(f'{parent_name} -MATED-> {entity.name} | CHILD: {child_name}')
    
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
    print(f"{entity.name} -SHARING FOOD-> {interaction_target['name']}")
    update_environment(environment=environment, entity=entity, interaction_target=interaction_target)

def interact_HEAL_OTHER(environment, entity):
    interaction_target = closest_node(environment, entity)
    if interaction_target is None:
        return
    if not interaction_target['is_Alive']:
        return
    if not (entity.energy > 5):
        return
    environment['healing_interactions'] = environment['healing_interactions'] + [entity.position, interaction_target['position']]
    entity.energy -= 5
    entity.food -= 2
    interaction_target['health'] += 20
    print(f"{entity.name} -HEALING-> {interaction_target['name']}")
    update_environment(environment=environment, entity=entity, interaction_target=interaction_target)
    
def interact_HUNT(environment, entity):
    interaction_target = closest_node(environment, entity, distance_threshold=20)
    if interaction_target is None:
        return
    if not (interaction_target['is_Alive'] & (interaction_target['name'] == entity.name)):
        return
    if not (entity.energy > 5):
        return
    
    environment['hunt'] = environment['hunt'] + [entity.position, interaction_target['position']]
    entity.energy -= 5
    entity.liked -= (interaction_target['liked']+100) # Reduces 'liked' metric by how much the target was liked + 100
    entity.position = interaction_target['position'] # sets position of entity on top of target
    interaction_target['health'] = 0 # kills target
    interaction_target['is_Alive'] = False # kills target
    interaction_target['cause_of_death'] = 'Hunted' #cod huntedw
    entity.food += (interaction_target['food'] + interaction_target['health']*interaction_target['size']) # takes their food and some
    print(f"{entity.name} -HUNTED-> {interaction_target['name']}")
    update_environment(environment=environment, entity=entity, interaction_target=interaction_target)