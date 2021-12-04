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
    environment['up'] = environment['up'] + [entity.position]
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x-vel), int(y)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_DN(environment, entity):
    environment['dn'] = environment['dn'] + [entity.position]
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x+vel), int(y)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_L(environment, entity):
    environment['l'] = environment['l'] + [entity.position]
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x), int(y-vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)

def move_R(environment, entity):
    environment['r'] = environment['r'] + [entity.position]
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x), int(y+vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)

def move_UPR(environment, entity):
    environment['upr'] = environment['upr'] + [entity.position]
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x-vel), int(y+vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_UPL(environment, entity):
    environment['upl'] = environment['upl'] + [entity.position]
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x-vel), int(y-vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_DNR(environment, entity):
    environment['dnr'] = environment['dnr'] + [entity.position]
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x+vel), int(y+vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)
    
def move_DNL(environment, entity):
    environment['dnl'] = environment['dnl'] + [entity.position]
    entity.energy -= 1
    vel, x, y = entity.current_velocity, entity.position[0], entity.position[1]
    goal = [int(x+vel), int(y-vel)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)

def move_RANDOM(environment, entity):
    environment['random'] = environment['random'] + [entity.position]
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
    environment['forward'] = environment['forward'] + [entity.position]
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
    environment['reverse'] = environment['reverse'] + [entity.position]
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
    environment['halt'] = environment['halt'] + [entity.position]
    x, y = entity.position[0], entity.position[1]
    goal = [int(x), int(y)]
    if is_occupied(environment=environment, goal=goal):
        return
    entity.position = goal
    update_environment(environment=environment, entity=entity)