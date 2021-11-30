import random
import string

from Entity.model import Model
from Entity.genetics import *
from Entity.Actions import individual, interactions, movement


class Entity:
    """
        Entity class: Generates interactable entity objects [Ex. human, door, plant, monster, wall...]
    """
    def __init__(self, genome_length=10, properties=None):
        """
            Inner class declaration
        """
        self.Status # Updates Entity object status
        self.Brain # Entity Brain
        
        """
            External properties to load
        """
        self.properties = properties
        self.genome_length = genome_length
        
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
        self.genome = generate_genome_RAND2HEX(length_genome=self.genome_length)
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
            Action handling
        """
        def __init__(self, environment, Entity):
            self.Entity = Entity
            self.environment = environment
            
        def do_action(self, option=None):
            self.Entity.energy -= 1 #Subtracts 1 energy for movement
            # TODO check to make sure tile is not occupied, moves tile*velocity
            '''movement'''
            if option == 'UP':
                movement.move_UP(self.environment, self.Entity)
            if option == 'DN':
                movement.move_DN(self.environment, self.Entity)
            if option == 'L':
                movement.move_L(self.environment, self.Entity)
            if option == 'R':
                movement.move_R(self.environment, self.Entity)
            if option == 'UPR':
                movement.move_UPR(self.environment, self.Entity)
            if option == 'UPL':
                movement.move_UPL(self.environment, self.Entity)
            if option == 'DNR':
                movement.move_DNR(self.environment, self.Entity)
            if option == 'DNL':
                movement.move_DNL(self.environment, self.Entity)
            if option == 'RANDOM':
                movement.move_RANDOM(self.environment, self.Entity)
            if option == 'FORWARD':
                movement.move_FORWARD(self.environment, self.Entity)
            if option == 'REVERSE':
                movement.move_REVERSE(self.environment, self.Entity)
            if option == 'HALT':
                movement.move_HALT(self.environment, self.Entity)
            
            '''actions to other entities'''
            if option == 'ATTACK':
                interactions.interact_ATTACK(self.environment, self.Entity)
            if option == 'MATE':
                interactions.interact_MATE(self.environment, self.Entity)
            if option == 'SHARE_FOOD':
                interactions.interact_SHARE_FOOD(self.environment, self.Entity)
            if option == 'BURY':
                interactions.interact_BURY(self.environment, self.Entity)
            if option == 'HUNT':
                interactions.interact_HUNT(self.environment, self.Entity)
            if option == 'HEAL_OTHER':
                interactions.interact_HEAL_OTHER(self.environment, self.Entity)
            if option == 'PICK_PLANT':
                interactions.interact_PICK_PLANT(self.environment, self.Entity)
            if option == 'EAT_HUMAN':
                interactions.interact_EAT_HUMAN(self.environment, self.Entity)
            
            '''self goals'''
            if option == 'REST':
                individual.individual_REST(self.environment, self.Entity)
            
    class Brain:
        """
            Thinks for entity; Maybe add IQ so doors don't start walking around (?)
        """
        def __init__(self, Entity, Actions, environment):
            self.Entity = Entity
            self.Actions = Actions
            self.environment = environment
            self.input_neurons = None
            self.inner_neurons = None
            self.output_neurons = None
            
        def __load_neurons(self):
            """
                sensory neurons
                inter neurons
                output neurons
            """
            
            '''sensory neurons'''
            self.input_neurons = {
            # Self identifiers (sensory neurons)
            '0' : self.Entity.velocity/10, # speed
            '1' : self.Entity.direction/360, # direction(degrees)
            '2' : (self.Entity.age)/100, # age
            '3' : (self.Entity.size)/20, # size
            '4' : (self.Entity.strength)/100, # strength
            '5' : (self.Entity.health)/100, # health; constitution
            '6' : (self.Entity.children)/10, # children
            '7' : (self.Entity.food)/100, # food available
            '8' : (self.Entity.liked)/100, # are they liked or not
            '9' : (self.Entity.energy)/100, # how much energy do they have
            '10' : (self.Entity.job_tasks)/100, # how many times have they done their job
            '11' : [1 if self.Entity.is_starving else -1][0], # are they starving
            '12' : [1 if self.Entity.can_mate else -1][0], # are they able to mate
            
            # random neurons and sensory mutations
            '13' : random.random(), # random values
            '14' : random.getrandbits(1), # random bits
            
            # external identifiers
            ## Blockage x, y
            ## Population x, y
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
                '0': 'UP',
                '1': 'DN',
                '2': 'L',
                '3': 'R',
                '4': 'UPR',
                '5': 'UPL',
                '6': 'DNR',
                '7': 'DNL',
                '8': 'RANDOM',
                '9': 'FORWARD',
                '10': 'REVERSE',
                '11': 'HALT',
                '12': 'ATTACK',
                '13': 'MATE',
                '14': 'REST',
                '15': 'SHARE_FOOD',
                '16': 'BURY',
                '17': 'HUNT',
                '18': 'HEAL_OTHER',
                '19': 'PICK_PLANT',
                '20': 'EAT_HUMAN',
            }
            
        def __build_brain_connections(self):
            instructions = translate_genome_HEX2OUT(genome=self.Entity.genome) # loads instructions for brain
            self.Entity.brain = [[(['input' if (instructions[connection]['source_type'])==1 else 'inner'][0]),
               (instructions[connection]['source_ID']%[len(self.inner_neurons) if instructions[connection]['source_ID']==0 else len(self.input_neurons)][0]),
               (['output' if (instructions[connection]['sink_type'])==1 else 'inner'][0]),
               ((instructions[connection]['source_ID'])%([len(self.inner_neurons) if instructions[connection]['source_ID']==0 else len(self.output_neurons)][0])),
               (instructions[connection]['weight'])] for connection in instructions]
            
        def __prune_connections(self):
            pruned_brain = []
            brain_input_section = [connections[0:2] for connections in self.Entity.brain]
            brain_output_section = [connections[2:4] for connections in self.Entity.brain]

            for connection in self.Entity.brain:
                # Trims inner connections with no final connection
                if connection[2] == 'inner': # If hidden layer exists. in --> hidden
                    if connection[2:4] not in brain_input_section:
                        continue

                # Trims inner connections with no starter connection, random noise/zero value
                if connection[0] == 'inner': # If hidden layer exists. hidden --> out
                    if connection[0:2] not in brain_output_section:
                        continue

                # Trims loops that have no input and output
                if (connection[0:2] == connection[2:4]) & (connection[0] == connection[2] == 'inner'):
                    if ~((connection[0:2] in brain_output_section) & (connection[2:4] in brain_input_section)):
                        continue
                    
                pruned_brain.append(connection)
            self.Entity.brain = pruned_brain

        def think(self): # come to a decision
            self.__load_neurons() # loads neuron values
            
            if self.Entity.brain is None: # generates brain if one doesn't exist
                self.__build_brain_connections()
                self.__prune_connections()
            
            choice = Model(brain=self.Entity.brain,
                           input_neurons=self.input_neurons,
                           inner_neurons=self.inner_neurons,
                           output_neurons=self.output_neurons).compile_and_run()
            if choice['brain_status'] == 'ERROR':
                return
            
            self.Actions.do_action(option=self.output_neurons[choice['brain_status']])

    '''NPC Commit Next Step'''
    def next(self, environment):
        if self.Status(Entity=self).update_status()['status'] == 'dead':
            return
        
        self.Brain(Entity=self,
                   Actions=self.Actions(environment=environment, Entity=self),
                   environment=environment
                   ).think()