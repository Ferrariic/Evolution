from os import environ
from Entity.entity import Entity 
from Environment.environment import Environment
from Environment.rebuild_generation import Generation
from Image.draw_screen import DrawImage
from Environment.filter import Filter
import json

starting_population = 100
lower_bound_threshold = int(starting_population/2)

step_years = 300
generation_cycles = 10000
genome_length = 300
world_size=[[-256, 256],[-256, 256]]

actions=True # See entity actions
load_latest=False # New file

if __name__ == '__main__':
    draw = DrawImage(world_size=world_size)
    
    if load_latest: # Loads the latest savefile
        environment = json.load(open('src\World\Data\data.json'))
        entities = Entity.update_entity_values(environment=environment, world_size=world_size)
    else: # Otherwise, builds new entity object list
        entities = [Entity(genome_length=genome_length) for entity in range(starting_population)]
        
    for generation in range(generation_cycles):
        for year in range(step_years):
            
            '''Exports current environment variables'''
            environment = Environment(environment_json=[entity.export_entity_values() for entity in entities]).export_environment_variables()
            '''Entities perform actions and update environment'''
            [entity.next(environment) for entity in entities] # entities do actions
            '''Draw environment to screen'''
            draw.draw_environment(environment=environment,generation=generation, year=year, actions=actions) 
            '''Check to see if failsafe needs to be triggered, lower population bound hit.'''
            if len(environment['environment_json']) <= lower_bound_threshold:
                break
            
            '''Update entities based upon the environment'''
            entities = Entity.update_entity_values(environment=environment, world_size=world_size) # update environment entities
        
        '''Optional filter'''
        entities = Filter(entities=entities).filter_population()
        
        '''Generation statistics'''
        Generation(entities=entities, population_limit=starting_population).statistics()
        '''Rebuilding the population after each generation based upon the survivors.'''
        entities = Generation(entities=entities, population_limit=starting_population).rebuild_population(environment=environment)