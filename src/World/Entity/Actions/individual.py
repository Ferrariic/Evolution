import math
from os import environ
from Entity.genetics import *

def update_environment(environment, entity):
    name_position = environment['all_entity_names'].index(entity.name)
    environment['environment_json'][name_position] = entity.export_entity_values()

def individual_REST(environment, entity):
    environment['plant'] = environment['plant'] + [entity.position]
    entity.food += 2
    update_environment(environment, entity)
    
def individual_SELF_REPLICATE(environment, entity):
    if not ((entity.food >= 150)&(entity.energy >= 100)&(not entity.is_Male)&(entity.can_mate)):
        return
    entity.energy -= 100
    entity.food -= 100
    entity.children += 1
    
    '''builds child'''
    new_entity = mate_parents_OBJ_OBJ(entity1=entity ,entity2=entity)
    child_name = new_entity['name']
    print(f'{entity.name} -SELF-REPLICATE-> {entity.name} | CHILD: {child_name}')
    
    update_environment(environment, entity) 
    environment['mate_interactions'] = environment['mate_interactions'] + [entity.position]
    environment['environment_json'].append(new_entity)