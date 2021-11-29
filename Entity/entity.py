import random
import string

from Genetics.genetics import *

class Entity:
    """
        Entity class: Generates interactable entity objects [Ex. human, door, plant, monster, wall...]
    """
    def __init__(self, properties=None):
        """
            Inner class declaration
        """
        self.Status # Updates Entity object status
        self.Brain # Entity Brain
        
        """
            External properties to load
        """
        self.properties = properties
        
        """
            Entity properties
        """
        # Name of entity
        self.name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12))
        self.entity_type = 'human'
        self.position = [random.randint(-10,10),random.randint(-10,10)]
        self.velocity = random.randint(1,30)
        self.direction = random.randint(0,359)
        self.is_alive = True
        self.is_Male = random.choice([True, False])
        self.will_Flee = random.choice([True, False])
        self.genome = generate_genome_RAND2HEX(length_genome=10)
        self.generation = 0
        self.age = 0
        self.size = 5
        self.strength = random.randint(30,50)
        self.health = random.randint(75,125)
        self.children = 0
        self.color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        self.food = random.randint(10,20)
        self.is_starving = False
        self.liked = 0
        self.goal = None
        self.job_tasks = 0
        self.energy = 100
        self.inventory = []
        self.can_mate = False
        self.brain = None
        self.cause_of_death = None
        
        if self.properties is not None:
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

    def export_entity_values(self):
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
    
    class Status:
        """
            Modifies status of Entity
        """
        def __init__(self, Entity):
            self.Entity = Entity
        
        def __check_is_alive(self):
            health_check = (self.Entity.health < 0)
            if health_check:
                self.Entity.is_alive = False
                return False
            return True
        
        def __check_can_mate(self):
            age_lower_bound_check = (self.Entity.age > 18)
            age_upper_bound_check = (self.Entity.age < 60)
            food_check = (self.Entity.food > 0)
            energy_check = (self.Entity.energy > 0)
            
            self.Entity.can_mate = False
            if age_lower_bound_check & age_upper_bound_check & food_check & energy_check:
                self.Entity.can_mate = True
                
        def __check_is_starving(self):
            food_check = self.Entity.food > 0
            self.Entity.is_starving = True
            if food_check:
                self.Entity.is_starving = False
                
        def __bound_stats(self):
            if self.Entity.energy > 100:
                self.Entity.energy = 100
            if self.Entity.energy < -100:
                self.Entity.energy = -100
                
            if self.Entity.liked > 100:
                self.Entity.liked = 100
            if self.Entity.liked < -100:
                self.Entity.liked = -100
                
            if self.Entity.food > 100:
                self.Entity.food = 100
                
            if self.Entity.health > 100:
                self.Entity.health = 100
                
            if self.Entity.strength > 100:
                self.Entity.strength = 100
            if self.Entity.strength < 0:
                self.Entity.strength = 0 
            
        def update_status(self):
            if not self.__check_is_alive():
                return {"status":"dead"}
            self.__check_can_mate()
            self.__check_is_starving()
            self.__bound_stats()
            return {"status":"alive"}

    class Actions:
        """
            Actions that an Entity can do to other Entities
        """
        def __init__(self, environment, Entity):
            self.Entity = Entity
            self.environment = environment
        
        def attack(self):
            self.Entity.energy -= 2 # Subtracts 1 energy for attacking
            # TODO
            return
        
        def mate(self):
            self.Entity.energy -= 2 # Subtracts 1 energy for mating
            # TODO
            return
        
        def rest(self):
            self.Entity.energy += 5 # Adds 5 energy for resting
            # TODO
            return
        
        def share_food(self):
            # TODO
            return
        
        def bury(self):
            # TODO
            return
        
        def hunt(self):
            # TODO
            return
        
        def heal_other(self):
            # TODO
            return
        
        def pick_plant(self):
            # TODO
            return
        
        def eat_human(self):
            # TODO
            return
        
        
    class Pathfinding:
        """
            Movement handling
        """
        def __init__(self, environment, Entity):
            self.Entity = Entity
            self.environment = environment
            
        def move(self, direction=None):
            self.Entity.energy -= 1 #Subtracts 1 energy for movement
            # TODO check to make sure tile is not occupied, moves tile*velocity
            if direction == 'UP':
                return
            if direction == 'DN':
                return
            if direction == 'L':
                return
            if direction == 'R':
                return
            if direction == 'UPR':
                return
            if direction == 'UPL':
                return
            if direction == 'DNR':
                return
            if direction == 'DNL':
                return
            if direction == 'RANDOM':
                return
            if direction == 'FORWARD':
                return
            if direction == 'REVERSE':
                return
            if direction == 'HALT':
                return
            
            
    class Brain:
        """
            Thinks for entity; Maybe add IQ so doors don't start walking around (?)
        """
        def __init__(self, Entity, Pathfinding, Actions, environment):
            self.Entity = Entity
            self.Pathfinding = Pathfinding
            self.Actions = Actions
            self.environment = environment
            self.input_neurons = None
            self.inner_neurons = None
            self.output_neurons = None
            
        def __organs(self):
            """
                sensory neurons
                inter neurons
                output neurons
            """
            
            '''sensory neurons'''
            self.input_neurons = {
            # Self identifiers (sensory neurons)
            '0' : self.Entity.velocity/10,
            '1' : self.Entity.direction/360,
            '2' : (self.Entity.age)/100,
            '3' : (self.Entity.size)/20,
            '4' : (self.Entity.strength)/100,
            '5' : (self.Entity.health)/100,
            '6' : (self.Entity.children)/10,
            '7' : (self.Entity.food)/100,
            '8' : (self.Entity.liked)/100,
            '9' : (self.Entity.energy)/100,
            '10' : (self.Entity.job_tasks)/100,
            '11' : [1 if self.Entity.is_starving else -1][0],
            '12' : [1 if self.Entity.can_mate else -1][0],
            
            # random neurons and sensory mutations
            '13' : random.random(),
            '14' : random.getrandbits(1),
            
            # external identifiers
            ## Blockage x, y
            ## Population x, y
            ## Total population
            ## Total enemies
            ## Total plants
            ## Total Other
            ## Proximity to next friend x, y
            ## Proximity to next enemy x, y
            ## Proximity to next plant x, y
            ## Proximity to next entity that can be mated x, y
            ## Proximity to next entity that can be fought x, y
            ## Proximity to world edge x, y
            }

            '''inner neurons'''
            # Establish inner neurons and their goals
            self.inner_neurons = {
                '0':random.random(),
                '1':random.random(),
                '2':random.random(),
                '3':random.random(),
                '4':random.random(),
                '5':random.random(),
                '6':random.random(),
                '7':random.random(),
                '8':random.random(),
                '9':random.random(),
            }
            
            
            '''output neurons'''
            # Establish motor neurons and their outputs
            self.output_neurons = {
                '0': self.Pathfinding.move(direction='UP'),
                '1': self.Pathfinding.move(direction='DN'),
                '2': self.Pathfinding.move(direction='L'),
                '3': self.Pathfinding.move(direction='R'),
                '4': self.Pathfinding.move(direction='UPR'),
                '5': self.Pathfinding.move(direction='UPL'),
                '6': self.Pathfinding.move(direction='DNR'),
                '7': self.Pathfinding.move(direction='DNL'),
                '8': self.Pathfinding.move(direction='RANDOM'),
                '9': self.Pathfinding.move(direction='FORWARD'),
                '10': self.Pathfinding.move(direction='REVERSE'),
                '11': self.Pathfinding.move(direction='HALT'),
                '12': self.Actions.attack(),
                '13': self.Actions.mate(),
                '14': self.Actions.rest(),
                '15': self.Actions.share_food(),
                '16': self.Actions.bury(),
                '17': self.Actions.hunt(),
                '18': self.Actions.heal_other(),
                '19': self.Actions.pick_plant(),
                '20': self.Actions.eat_human(),
            }
            
        def __build_brain_network(self):
            self.__organs() # loads organs
            instructions = translate_genome_HEX2OUT(genome=self.Entity.genome) # loads instructions for brain
            ## TODO turn instructions into neural network and take compute as final output rule
            print(instructions)

        def think(self): # come to a decision
            if self.Entity.brain is None:
                self.__build_brain_network()
    
    '''NPC Commit Next Step'''
    def next(self, environment):
        if self.Status(Entity=self).update_status()['status'] == 'dead':
            return
        self.Brain(Entity=self,
                   Pathfinding=self.Pathfinding(environment=environment, Entity=self),
                   Actions=self.Actions(environment=environment, Entity=self),
                   environment=environment
                   ).think()
        

entities = [Entity() for entity in range(1)]
environment = [entity.export_entity_values() for entity in entities]
environment = [entity.next(environment) for entity in entities]
