from os import environ
from Entity.entity import Entity 
from Environment.environment import Environment
from Environment.rebuild_generation import Generation
from Image.draw_screen import DrawImage
from Environment.filter import Filter

starting_population = 200
lower_bound_threshold = int(starting_population/4)
step_years = 300
generation_cycles = 10000
world_size=[[-128, 128],[-128, 128]]

draw = DrawImage(world_size=world_size)
entities = [Entity(genome_length=10) for entity in range(starting_population)]
if __name__ == '__main__':
    for generation in range(generation_cycles):
        for year in range(step_years):
            environment = Environment(environment_json=[entity.export_entity_values() for entity in entities]).export_environment_variables() # export environment
            draw.draw_environment(environment=environment)
            if len(environment['environment_json']) <= lower_bound_threshold:
                population = len(environment['environment_json'])
                print(f"----------------------{generation=}---{year=}---{population=}----------------------")
                break
            
            [entity.next(environment) for entity in entities] # entities do actions
            entities = Entity.update_entity_values(environment=environment, world_size=world_size) # update environment entities
        
        population = len(environment['environment_json'])
        print(f"----------------------{generation=}---{year=}---{population=}----------------------")
        #entities = Filter(entities=entities).filter_population()
        
        Generation(entities=entities, population_limit=starting_population).statistics()
        entities = Generation(entities=entities, population_limit=starting_population).rebuild_population()