import math
import random

"""
    movement backup functions
    -y/+y = down/up
    -x/+x = left/right
"""
def is_occupied(environment, goal):
    locations = environment['all_entity_locations']
    if goal in locations:
        return True
    return False

def update_environment(environment, entity):
    name_position = environment['all_entity_names'].index(entity.name)
    environment['environment_json'][name_position] = entity.export_entity_values()
    
'''movement functions'''
def move_UP(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x), int(y+vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_DN(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x), int(y-vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_L(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x-vel), int(y)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)

def move_R(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x+vel), int(y)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)

def move_UPR(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x+vel), int(y+vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_UPL(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x-vel), int(y+vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_DNR(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x+vel), int(y-vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_DNL(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x-vel), int(y-vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)

def move_RANDOM(environment, entity):
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    x_rand = int(([-1,1][random.randrange(2)])*random.random()*vel)
    y_rand = int(([-1,1][random.randrange(2)])*random.random()*vel)
    goal = [int(x+x_rand), int(y+y_rand)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_FORWARD(environment, entity):
    entity.energy -= 1
    direction, vel, x, y = entity.direction, entity.current_velocity, entity.position[0], entity.position[1]
    x1 = int(math.cos(math.radians(direction))*vel)
    y1 = int(math.sin(math.radians(direction))*vel)
    goal = [int(x+x1), int(y+y1)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_REVERSE(environment, entity):
    entity.energy -= 1
    direction, vel, x, y = entity.direction, entity.current_velocity, entity.position[0], entity.position[1]
    x1 = int(math.cos(math.radians(direction))*-vel)
    y1 = int(math.sin(math.radians(direction))*-vel)
    goal = [int(x+x1), int(y+y1)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_HALT(environment, entity):
    x, y = entity.position[0], entity.position[1]
    goal = [int(x), int(y)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
