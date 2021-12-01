import collections
import random
from Entity.genetics import *
from Entity.entity import Entity
import json

class Generation:
    def __init__(self, entities, population_limit) -> list:
        self.entities = entities
        self.population_limit = population_limit
        self.genetic_distribution = None
     
    def rebuild_population(self, environment):
        entity_list = []
        while len(entity_list) < self.population_limit:
            try:
                entity1, entity2 = random.choices(self.entities, k=2)
            except:
                print("Population could not be rebuilt.")
            new_ent_dict = mate_parents_OBJ_OBJ(entity1=entity1, entity2=entity2)
            entity_list.append(Entity(properties=new_ent_dict))
            
        with open("src/World/Data/data.json", 'w') as f:
            json.dump(environment, f)
        return entity_list
        
    def statistics(self):
        genetic_pool = [entity.genome for entity in self.entities]
        gene_lists = [genome.split(' ') for genome in genetic_pool]
        genes = [gene for entity_genes in gene_lists for gene in entity_genes]
        Unique_genes = len(set(genes))
        print(f'{Unique_genes=}')
        