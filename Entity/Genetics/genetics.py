import random
import numpy as np
import textwrap

'''generate random genome of length n'''
def generate_genome_RAND2HEX(length_genome=10):
    return ' '.join([hex(int(''.join([str(random.getrandbits(1)) for bit in range(32)]),2)) for gene in range(length_genome)])

'''decode from DNA_HEX into RNA_BIN'''
def decode_genome_HEX2BIN(genome, mutate=True):
    bingenome = [bin(int(hexgene,16))[2:].zfill(32) for hexgene in genome.split(' ')]
    if mutate:
        bingenome = textwrap.wrap(''.join([str(1-int(bit)) if (random.randint(1, 25)==1) else bit for gene in bingenome for bit in gene]), 32)
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
    DNA1 = genome1.split(' ')
    DNA2 = genome2.split(' ')
    length = int((len(DNA1)+len(DNA2))/2)
    pool = DNA1+DNA2
    return ' '.join(list(set(random.choices(pool, k=length))))