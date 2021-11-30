class Status:
    """
        Modifies internal status of Entity
    """
    def __init__(self, properties):
        self.properties = properties
        
        self.name = self.properties['name']
        self.entity_type = self.properties['entity_type']
        self.position = self.properties['position']
        self.velocity = self.properties['velocity']
        self.direction = self.properties['direction']
        self.is_alive = self.properties['is_Alive']
        self.is_Male = self.properties['is_Male']
        self.will_Flee = self.properties['will_Flee']
        self.genome = self.properties['genome']
        self.generation =  self.properties['generation']
        self.age = self.properties['age']
        self.size = self.properties['size']
        self.strength = self.properties['strength']
        self.health = self.properties['health']
        self.children = self.properties['children']
        self.color = self.properties['color']
        self.food = self.properties['food']
        self.is_starving = self.properties['is_starving']
        self.liked = self.properties['liked']
        self.goal = self.properties['goal']
        self.job_tasks = self.properties['job_tasks']
        self.energy = self.properties['energy']
        self.inventory = self.properties['inventory']
        self.can_mate = self.properties['can_mate']
        self.brain = self.properties['brain']
        self.cause_of_death = self.properties['cause_of_death']
    
    def __check_is_alive(self):
        health_check = (self.health < 0)
        if health_check:
            self.is_alive = False
            return False
        return True
    
    def __check_can_mate(self):
        age_lower_bound_check = (self.age > 18)
        food_check = (self.food > 0)
        energy_check = (self.energy > 0)
        
        self.can_mate = False
        if age_lower_bound_check & food_check & energy_check:
            self.can_mate = True
            
    def __check_is_starving(self):
        food_check = self.food > 0
        self.is_starving = True
        if food_check:
            self.is_starving = False
            
    def __bound_stats(self):
        if self.energy > 100:
            self.energy = 100
        if self.energy < 0:
            self.energy = 0
            
        if self.liked > 100:
            self.liked = 100
        if self.liked < -100:
            self.liked = -100
            
        if self.food > 200:
            self.food = 200
        if self.food < 0:
            self.food = 0
            
        if self.health > 100:
            self.health = 100
        if self.health < 0:
            self.health = 0
            
        if self.strength > 100:
            self.strength = 100
        if self.strength < 0:
            self.strength = 0
            
        ### Optional world bounds
        x, y = self.position[0], self.position[1]
        if (x>100):
            self.position[0]=100
        if (x<-100):
            self.position[0]=-100
        if (y>100):
            self.position[1]=100
        if (y<-100):
            self.position[1]=-100
            
    def __world_decay(self):
        '''constant decay states for the world'''
        self.food -= 1 # Subtract 1 food per cycle
        self.age += 1 # Add one age per cycle
        
    def __spend_stats(self):
        
        '''If the entity is weak, spend food to replenish energy'''
        if (self.energy < 10) & (self.food > 5):
            self.food -= 2
            self.energy += 20
        
        '''If the entity is starving and has 0 food, subtract health'''
        if self.food < 1:
            self.health -= 5
            self.energy -= 5

        '''If the entity is starving and has 0 food, subtract health'''
        if (self.health < 50) & (self.food > 2) & (self.energy > 5) :
            self.food -= 2
            self.energy -= 5
            self.health += 5
            
    def __export_entity_values(self):
        properties = {
            'name':self.name,
            'entity_type':self.entity_type,
            'position':self.position,
            'velocity':self.velocity,
            'direction':self.direction,
            'is_Alive':self.is_alive,
            'is_Male':self.is_Male,
            'will_Flee':self.will_Flee,
            'genome':self.genome,
            'generation':self.generation,
            'age':self.age,
            'size':self.size,
            'strength':self.strength,
            'health':self.health,
            'children':self.children,
            'color':self.color,
            'food':self.food,
            'is_starving':self.is_starving,
            'liked':self.liked,
            'goal':self.goal,
            'job_tasks':self.job_tasks,
            'energy':self.energy,
            'inventory':self.inventory,
            'can_mate':self.can_mate,
            'brain':self.brain,
            'cause_of_death':self.cause_of_death,
        }
        return properties
                
    def update_status(self):
        self.__world_decay() # world stats reduced per cycle
        self.__spend_stats() # stat upkeep
        if not self.__check_is_alive(): # checks if dead
            return {"status":"dead"}
        self.__check_can_mate() # checks if can mate
        self.__check_is_starving() # checks if starving
        self.__bound_stats() # bounds stats depending on if out of range
        return {"status": self.__export_entity_values()}