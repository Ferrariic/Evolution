import math

"""
    Movement functions
"""

def move_UP(environment, entity):
    entity.energy -= 1
    print("moving up")
    
def move_DN(environment, entity):
    entity.energy -= 1
    print('moving down')
    
def move_L(environment, entity):
    entity.energy -= 1
    print('moving left')

def move_R(environment, entity):
    entity.energy -= 1
    print('moving right')

def move_UPR(environment, entity):
    entity.energy -= 1
    print('moving up right')
    
def move_UPL(environment, entity):
    entity.energy -= 1
    print('moving up left')
    
def move_DNR(environment, entity):
    entity.energy -= 1
    print('moving down right')
    
def move_DNL(environment, entity):
    entity.energy -= 1
    print('moving down left')

def move_RANDOM(environment, entity):
    entity.energy -= 1
    print('moving randomly')
    
def move_FORWARD(environment, entity):
    entity.energy -= 1
    print('moving forward')
    
def move_REVERSE(environment, entity):
    entity.energy -= 1
    print('moving reverse')
    
def move_HALT(environment, entity):
    print('halting movement')