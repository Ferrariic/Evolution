import collections
import random
from Entity.genetics import *
from Entity.entity import Entity

class Generation:
    def __init__(self, entities, population_limit) -> list:
        self.entities = entities
        self.population_limit = population_limit
        self.genetic_distribution = None
     
    def rebuild_population(self):
        entity_list = []
        while len(entity_list) < self.population_limit:
            entity1, entity2 = random.choices(self.entities, k=2)
            new_ent_dict = mate_parents_OBJ_OBJ(entity1=entity1, entity2=entity2)
            entity_list.append(Entity(properties=new_ent_dict))
        return entity_list
    
    def __examine_connections(self):
        genome_pool = []
        for key, values, in self.genetic_distribution.items():
            genome_pool.append(key)
        
        genome_pool = ' '.join(genome_pool)
        instructions = translate_genome_HEX2OUT(genome_pool)
        print(instructions)
        
    def statistics(self):
        genetic_pool = [entity.genome for entity in self.entities]
        gene_lists = [genome.split(' ') for genome in genetic_pool]
        genes = [gene for entity_genes in gene_lists for gene in entity_genes]
        self.genetic_distribution = dict(collections.Counter(genes))
        Unique_genes = len(set(genes))
        print(f'{Unique_genes=}', self.genetic_distribution)
        #self.__examine_connections()
        