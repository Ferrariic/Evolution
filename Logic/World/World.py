from Entity.entity import Entity 
from Environment.environment import Environment


entities = [Entity(genome_length=100) for entity in range(10)]
if __name__ == '__main__':
    for year in range(10):
        environment = Environment(environment_json=[entity.export_entity_values() for entity in entities]).export_environment_variables()
        [entity.next(environment) for entity in entities]