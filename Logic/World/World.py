from Entity.entity import Entity 
from Environment.environment import Environment
from Environment.rebuild_generation import Generation

starting_population = 100
lower_bound_threshold = 10
step_years = 250
generation_cycles = 100

entities = [Entity(genome_length=10) for entity in range(starting_population)]
if __name__ == '__main__':
    for generation in range(generation_cycles):
        for year in range(step_years):
            environment = Environment(environment_json=[entity.export_entity_values() for entity in entities]).export_environment_variables() # export environment
            [entity.next(environment) for entity in entities] # entities do actions
            entities = Entity.update_entity_values(environment=environment) # update environment entities
            if len(environment['environment_json']) <= lower_bound_threshold:
                print("Population low-limit reached. Breaking.")
                break
            print(f"year: {year}, population {len(environment['environment_json'])}")
        print(f"Generation {generation} completed. Population: {len(environment['environment_json'])}")
        entities = Generation(entities=entities, population_limit=starting_population).rebuild_population()
        Generation(entities=entities, population_limit=starting_population).statistics()