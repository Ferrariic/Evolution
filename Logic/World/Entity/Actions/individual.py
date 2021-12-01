import math
from os import environ

def update_environment(environment, entity):
    name_position = environment['all_entity_names'].index(entity.name)
    environment['environment_json'][name_position] = entity.export_entity_values()

def individual_REST(environment, entity):
    entity.energy += 50
    entity.food += 3
    update_environment(environment, entity)