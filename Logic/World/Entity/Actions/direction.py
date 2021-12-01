
"""
    Change direction that entity is looking (movement, maybe interactions?)
"""

def normalize_direction(degrees):
    return degrees % 360
    
def change_direction_RIGHT(environment, entity):
    entity.direction = normalize_direction((entity.direction - 45))

def change_direction_LEFT(environment, entity):
    entity.direction = normalize_direction((entity.direction + 45))

def change_direction_REVERSE(environment, entity):
    entity.direction = normalize_direction((entity.direction - 180))

def change_direction_REDUCE_VELOCITY(environment, entity):
    entity.current_velocity -= 1
    if entity.current_velocity < 0:
        entity.current_velocity = 0

def change_direction_INCREASE_VELOCITY(environment, entity):
    entity.current_velocity += 1
    if entity.current_velocity > entity.velocity:
        entity.current_velocity = entity.velocity