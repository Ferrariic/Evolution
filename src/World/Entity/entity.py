import random
import string
from os import environ

from Entity.Actions import direction, individual, interactions, movement
from Entity.genetics import *
from Entity.model import Model
from Entity.status import Status
from Entity.Sensors.sensors import Sensors

class Entity:
    """
        Entity class: Generates interactable entity objects [Ex. human, door, plant, monster, wall...]
    """
    def __init__(self, genome_length=10, properties=None):
        """
            Inner class declaration
        """
        self.Brain # Entity Brain
        
        """
            External properties to load
        """
        self.properties = properties
        self.genome_length = genome_length
        
        """
            Entity properties
        """
        
        '''random name given'''
        self.name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12))
        
        '''genetic assignments'''
        self.genome = generate_genome_RAND2HEX(length_genome=self.genome_length)
        self.velocity = assign_velocity_HEX2INT(self.genome)
        self.is_Male = assign_male_HEX2BOOL(self.genome)
        self.will_Flee = assign_flee_HEX2BOOL(self.genome)
        self.image = assign_image_8X8(self.genome)
        self.size = assign_size_HEX2INT7(self.genome)
        self.strength = assign_strength_HEX2INT63(self.genome)
        self.health = assign_health_HEX2INT127(self.genome)
        
        '''world properties'''
        self.position = [random.randint(-256,256),random.randint(-256,256)]
        self.direction = random.randint(0,359)
        self.current_velocity = self.velocity
        
        '''self properties'''
        self.inventory = []
        self.food = random.randint(80,100)
        self.energy = 100
        self.liked = 0
        self.children = 0
        self.generation = 0
        self.age = 0    
        self.is_starving = False
        self.can_mate = False
        self.is_alive = True
        self.brain = None
        self.cause_of_death = None
        
        if self.properties is not None:
            self.name = self.properties['name']
            self.genome = self.properties['genome']
            self.position = self.properties['position']
            self.velocity = self.properties['velocity']
            self.current_velocity = self.properties['current_velocity']
            self.direction = self.properties['direction']
            self.is_alive = self.properties['is_Alive']
            self.is_Male = self.properties['is_Male']
            self.will_Flee = self.properties['will_Flee']
            self.generation =  self.properties['generation']
            self.age = self.properties['age']
            self.size = self.properties['size']
            self.strength = self.properties['strength']
            self.health = self.properties['health']
            self.children = self.properties['children']
            self.image = self.properties['image']
            self.food = self.properties['food']
            self.is_starving = self.properties['is_starving']
            self.liked = self.properties['liked']
            self.energy = self.properties['energy']
            self.inventory = self.properties['inventory']
            self.can_mate = self.properties['can_mate']
            self.brain = self.properties['brain']
            self.cause_of_death = self.properties['cause_of_death']

    def export_entity_values(self):
        properties = {
            'name':self.name,
            'position':self.position,
            'velocity':self.velocity,
            'current_velocity':self.current_velocity,
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
            'image':self.image,
            'food':self.food,
            'is_starving':self.is_starving,
            'liked':self.liked,
            'energy':self.energy,
            'inventory':self.inventory,
            'can_mate':self.can_mate,
            'brain':self.brain,
            'cause_of_death':self.cause_of_death,
        }
        return properties
    
    def update_entity_values(environment, world_size):
        status_list = []
        for entity in environment['environment_json']:
            entity_properties = Status(entity, world_size=world_size).update_status()['status']
            if entity_properties == 'dead':
                continue
            status_list.append(entity_properties)
        return [Entity(properties=entity) for entity in status_list] # generates new entities
        
    class Actions:
        """
            Action handling
        """
        def __init__(self, environment, Entity):
            self.Entity = Entity
            self.environment = environment
            
        def do_action(self, option=None):
            if not ((self.Entity.energy > 1) & (self.Entity.is_alive)):
                return
            
            '''direction'''
            if option == 'DIR_RIGHT':
                direction.change_direction_RIGHT(self.environment, self.Entity)
            if option == 'DIR_LEFT':
                direction.change_direction_LEFT(self.environment, self.Entity)
            if option == 'DIR_REVERSE':
                direction.change_direction_REVERSE(self.environment, self.Entity)
            if option == 'VEL_REDUCE':
                direction.change_direction_REDUCE_VELOCITY(self.environment, self.Entity)
            if option == 'VEL_INCREASE':
                direction.change_direction_INCREASE_VELOCITY(self.environment, self.Entity)
            
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
            if option == 'HUNT':
                interactions.interact_HUNT(self.environment, self.Entity)
            if option == 'HEAL_OTHER':
                interactions.interact_HEAL_OTHER(self.environment, self.Entity)
            
            '''self goals'''
            if option == 'REST':
                individual.individual_REST(self.environment, self.Entity)
            if option == 'SELF_REPLICATE':
                individual.individual_SELF_REPLICATE(self.environment, self.Entity)
            
    class Brain:
        """
            Thinks for entity;
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
            sensor = Sensors(entity=self.Entity, environment=self.environment)
            x_proximity, y_proximity = sensor.proximity_to_neighbor_XY()
            x_density, y_density = sensor.population_XY()
            x_distance_mate, y_distance_mate = sensor.proximity_to_mate_XY()
            
            '''sensory neurons'''
            self.input_neurons = {
            # Self identifiers
            '0' : sensor.velocity(), # velocity of subject
            '1' : sensor.current_velocity(), # current velocity of subject
            '2' : sensor.direction(), # direction of subject motion
            '3' : sensor.age(), # age of subject
            '4' : sensor.size(), # size of subject
            '5' : sensor.strength(), # strength
            '6' : sensor.health(), # health; constitution
            '7' : sensor.children(), # children
            '8' : sensor.food(), # food available
            '9' : sensor.liked(), # are they liked or not
            '10' : sensor.energy(), # how much energy do they have
            '11' : sensor.starving(), # are they starving
            '12' : sensor.mate(), # are they able to mate
            
            # random neurons and sensory mutations
            '13' : random.random(), # random values
            
            # Population identifiers
            '14' : x_proximity, # proximity to neighbor
            '15' : y_proximity, ## proximity to neighbor
            '16' : sensor.direction_to_neighbor(),
            '17' : x_density, # density in x direction
            '18' : y_density, # density in y direction
            '19' : x_distance_mate, # x distance to mate
            '20' : y_distance_mate, # y distance to mate
            }

            '''inner neurons'''
            # Establish inner neurons and their goals
            INNER_NEURONS = 1
            self.inner_neurons = {str(key):0 for key in range(INNER_NEURONS)}
            
            '''output neurons'''
            # Establish motor neurons and their outputs
            MOVEMENT_OUTPUTS = ['UP','DN','L','R','UPR','UPL','DNR','DNL','RANDOM','REVERSE','FORWARD','HALT']
            DIRECTION_VELOCITY_OUTPUTS = ['DIR_RIGHT','DIR_LEFT','DIR_REVERSE','VEL_REDUCE','VEL_INCREASE']
            INTERACTION_OUTPUTS = ['ATTACK','HUNT'] #'SHARE_FOOD','HEAL_OTHER',
            INDIVIDUAL_OUTPUTS = ['REST']
            MATE_OUTPUTS = ['MATE','SELF_REPLICATE']

            OUTPUTS = MOVEMENT_OUTPUTS+\
                    DIRECTION_VELOCITY_OUTPUTS+\
                    INTERACTION_OUTPUTS+\
                    INDIVIDUAL_OUTPUTS+MATE_OUTPUTS
            self.output_neurons = {str(key):value for key,value in enumerate(OUTPUTS)}
            
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
        self.Brain(Entity=self,
                   Actions=self.Actions(environment=environment, Entity=self),
                   environment=environment
                   ).think()
