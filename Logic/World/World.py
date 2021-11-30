from Entity.entity import Entity 
from Environment.environment import Environment


entities = [Entity(genome_length=100) for entity in range(1000)]
if __name__ == '__main__':
    for year in range(10000):
        environment = Environment(environment_json=[entity.export_entity_values() for entity in entities]).export_environment_variables() # export environment
        [entity.next(environment) for entity in entities] # entities do actions
        entities = Entity.update_entity_values(environment=environment) # update environment entities
        print(f"year: {year}, population {len(environment['environment_json'])}")