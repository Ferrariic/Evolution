class Filter:
    def __init__(self, entities):
        self.entities = entities
    
    def __filter_LEFT(self):
        entity_list = []
        for entity in self.entities:
            if entity.position[1] > -100:
                continue
            entity_list.append(entity)
        self.entities = entity_list
        
    def __filter_DOWN(self):
        entity_list = []
        for entity in self.entities:
            if entity.position[0] < 100:
                continue
            entity_list.append(entity)
        self.entities = entity_list
    
    def filter_population(self):
        self.__filter_LEFT()
        self.__filter_DOWN()
        return self.entities