import random
import numpy as np
import textwrap
import string

'''generate random genome of length n'''
def generate_genome_RAND2HEX(length_genome=10):
    return ' '.join([hex(int(''.join([str(random.getrandbits(1)) for bit in range(32)]),2)) for gene in range(length_genome)])

'''decode from DNA_HEX into RNA_BIN'''
def decode_genome_HEX2BIN(genome, mutate=True):
    bingenome = [bin(int(hexgene,16))[2:].zfill(32) for hexgene in genome.split(' ')]
    if mutate:
        bingenome = textwrap.wrap(''.join([str(1-int(bit)) if (random.randint(1, 128)==1) else bit for gene in bingenome for bit in gene]), 32)
    return bingenome

'''encoding from bin to hex'''
def encode_genome_BIN2HEX(genome):
    return ' '.join([hex(int(bitgene, 2)) for bitgene in genome])

'''translating into neural network linkages'''
def translate_genome_HEX2OUT(genome):
    # 0 - source type [0 - internal neuron, 1 - input neuron]
    # 1-8 - source ID [unsigned % number of neurons to tell which neuron]
    # 9 - sink type [0 - internal neuron, 1 - output neuron]
    # 10-16 - sink ID [unsigned % number of neurons to tell which neuron]
    # 17-32 - weight (divide to get actual)
    RNA = decode_genome_HEX2BIN(genome)
    instructions = dict()
    for connection_number, instruction in enumerate(RNA):
        instructions[connection_number] = {}
        instructions[connection_number]['source_type'] = int(instruction[0],2)
        instructions[connection_number]['source_ID'] = int(instruction[1:8],2)
        instructions[connection_number]['sink_type'] = int(instruction[8],2)
        instructions[connection_number]['sink_ID'] = int(instruction[9:16],2)
        instructions[connection_number]['weight'] = int(instruction[16:33],2)/int('1111111111111111',2)*4*([-1,1][random.randrange(2)])
    return instructions
    
'''cross over for mating'''
def cross_over_HEX_A_HEX(genome1, genome2):
    def random_engine(genome1, genome2):
        DNA1 = encode_genome_BIN2HEX(decode_genome_HEX2BIN(genome1, mutate=True)).split(' ')
        DNA2 = encode_genome_BIN2HEX(decode_genome_HEX2BIN(genome2, mutate=True)).split(' ')

        pool = DNA1+DNA2
        cap = random.choice([DNA1[0],DNA2[0]])
        objective_length = int(((len(DNA1)+len(DNA2))/2)+random.randint(-1,1))
        if objective_length < 1:
            objective_length = 1

        genome = [cap]+random.choices(pool, k=objective_length)
        return genome
        
    def cross_over_engine(genome1, genome2):
        DNA1 = encode_genome_BIN2HEX(decode_genome_HEX2BIN(genome1, mutate=True)).split(' ')
        DNA2 = encode_genome_BIN2HEX(decode_genome_HEX2BIN(genome2, mutate=True)).split(' ')

        pool = DNA1+DNA2
        cap = random.choice([DNA1[0],DNA2[0]])
        objective_length = int(((len(DNA1)+len(DNA2))/2)+random.randint(-1,1))
        if objective_length < 1:
            objective_length = 1


        genome = [cap]+random.choice([DNA1[1:]+DNA2[1:],DNA2[1:]+DNA1[1:]])[:objective_length]
        return genome
    
    genome = cross_over_engine(genome1, genome2)
    return ' '.join(genome)


"""
    genetic assignment of properties [32 bool assignment] of first gene
    is_Male = pos 0
    will_Flee = pos 2
    velocity = pos 0:5
    health = pos 5:12
    strength = pos 12:18
    size = pos 24:27
    color:
        R - 0:8
        G - 8:16
        B - 16:24
"""
def assign_male_HEX2BOOL(genome):
    return [True if int(decode_genome_HEX2BIN(genome, mutate=False)[0][0])==1 else False][0]

def assign_flee_HEX2BOOL(genome):
    return [True if int(decode_genome_HEX2BIN(genome, mutate=False)[0][1])==1 else False][0]

def assign_health_HEX2INT127(genome):
    return int(decode_genome_HEX2BIN(genome, mutate=False)[0][5:12],2)+1

def assign_velocity_HEX2INT(genome):
    return int(decode_genome_HEX2BIN(genome, mutate=False)[0][0:5],2)+1

def assign_strength_HEX2INT63(genome):
    return int(decode_genome_HEX2BIN(genome, mutate=False)[0][12:18],2)+1

def assign_size_HEX2INT7(genome):
    return int(decode_genome_HEX2BIN(genome, mutate=False)[0][24:27],2)+1

def assign_color_HEX2TRIPLE255(genome):
    color1 = int(decode_genome_HEX2BIN(genome, mutate=False)[0][0:8],2)
    color2 = int(decode_genome_HEX2BIN(genome, mutate=False)[0][8:16],2)
    color3 = int(decode_genome_HEX2BIN(genome, mutate=False)[0][16:24],2)
    return [color1, color2, color3]

def assign_image_8X8(genome):
    half_img = np.asarray([1 if value == '1' else 0 for value in decode_genome_HEX2BIN(genome, mutate=False)[0]])
    half_img = np.stack([half_img, half_img, half_img],axis=1)
    half_img = half_img.reshape(-1,4,3)*255
    sprite = np.concatenate((half_img, np.fliplr(half_img)), axis=1)
    sprite = np.where(sprite>1, assign_color_HEX2TRIPLE255(genome), [0,0,0])
    return sprite.tolist()
"""
    Entity Creation for Crossover
"""

'''crosses parents for Interaction Mating'''
def mate_parents_OBJ_DICT(entity, interaction_target):
    new_entity = dict()
    new_entity['name'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12))
    new_entity['genome'] =  cross_over_HEX_A_HEX(entity.genome, interaction_target['genome'])
    new_entity['strength'] = assign_strength_HEX2INT63(new_entity['genome'])
    new_entity['health'] = assign_health_HEX2INT127(new_entity['genome'])
    new_entity['is_Male'] = assign_male_HEX2BOOL(new_entity['genome'])
    new_entity['size'] = assign_size_HEX2INT7(new_entity['genome'])
    new_entity['image'] = assign_image_8X8(new_entity['genome'])
    new_entity['velocity'] = assign_velocity_HEX2INT(new_entity['genome'])
    new_entity['current_velocity'] = new_entity['velocity'] 
    new_entity['will_Flee'] = assign_flee_HEX2BOOL(new_entity['genome'])
    new_entity['food'] = random.randint(80,100)
    new_entity['children'] = 0
    new_entity['direction'] = random.randint(0,359)
    new_entity['is_Alive'] = True
    new_entity['can_mate'] = False
    new_entity['energy'] = 100
    new_entity['age'] = 0
    new_entity['liked'] = 0
    new_entity['brain'] = None
    new_entity['is_starving'] = False
    new_entity['job_tasks'] = 0
    new_entity['inventory'] = []
    new_entity['position'] = entity.position
    new_entity['generation'] = int(max([entity.generation,interaction_target['generation']])+1)
    new_entity['cause_of_death'] = None
    return new_entity

'''mate parents for generational testing'''
def mate_parents_OBJ_OBJ(entity1, entity2):
    new_entity = dict()
    
    new_entity['name'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12))
    new_entity['genome'] =  cross_over_HEX_A_HEX(entity1.genome, entity2.genome)
    new_entity['velocity'] = assign_velocity_HEX2INT(new_entity['genome'])
    new_entity['will_Flee'] = assign_flee_HEX2BOOL(new_entity['genome'])
    new_entity['size'] = assign_size_HEX2INT7(new_entity['genome'])
    new_entity['strength'] = assign_strength_HEX2INT63(new_entity['genome'])
    new_entity['health'] = assign_health_HEX2INT127(new_entity['genome'])
    new_entity['image'] = assign_image_8X8(new_entity['genome'])
    new_entity['is_Male'] = assign_male_HEX2BOOL(new_entity['genome'])
    new_entity['current_velocity'] = new_entity['velocity'] 
    new_entity['food'] = random.randint(80,100)
    new_entity['generation'] = int(max([entity1.generation, entity2.generation])+1)
    new_entity['children'] = 0
    new_entity['direction'] = random.randint(0,359)
    new_entity['is_Alive'] = True
    new_entity['can_mate'] = False
    new_entity['energy'] = 100
    new_entity['age'] = 0
    new_entity['brain'] = None
    new_entity['is_starving'] = False
    new_entity['liked'] = 0
    new_entity['inventory'] = []
    new_entity['position'] = [random.randint(-256,256),random.randint(-256,256)]

    new_entity['cause_of_death'] = None
    return new_entity