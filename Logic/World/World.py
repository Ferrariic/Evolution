from os import environ
from Entity.entity import Entity 
from Environment.environment import Environment
from Environment.rebuild_generation import Generation
from Image.draw_screen import DrawImage

starting_population = 500
lower_bound_threshold = 200
step_years = 200
generation_cycles = 10
world_size=[[-300, 300],[-300, 300]]
draw = DrawImage(world_size=world_size)
entities = [Entity(genome_length=2) for entity in range(starting_population)]
if __name__ == '__main__':
    for generation in range(generation_cycles):
        for year in range(step_years):
            environment = Environment(environment_json=[entity.export_entity_values() for entity in entities]).export_environment_variables() # export environment
            draw.draw_environment(environment=environment)
            if len(environment['environment_json']) <= lower_bound_threshold:
                break
            
            [entity.next(environment) for entity in entities] # entities do actions
            entities = Entity.update_entity_values(environment=environment, world_size=world_size) # update environment entities
            print(f"year: {year}, population {len(environment['environment_json'])}")
            
        print(f"Generation {generation} completed. Population: {len(environment['environment_json'])}")
        Generation(entities=entities, population_limit=starting_population).statistics()
        entities = Generation(entities=entities, population_limit=starting_population).rebuild_population()