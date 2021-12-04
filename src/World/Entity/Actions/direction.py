
"""
    Change direction that entity is looking (movement, maybe interactions?)
"""

def normalize_direction(degrees):
    return degrees % 360
    
def change_direction_RIGHT(environment, entity):
    environment['changing_values'] = environment['changing_values'] + [entity.position]
    entity.direction = normalize_direction((entity.direction - 45))

def change_direction_LEFT(environment, entity):
    environment['changing_values'] = environment['changing_values'] + [entity.position]
    entity.direction = normalize_direction((entity.direction + 45))

def change_direction_REVERSE(environment, entity):
    environment['changing_values'] = environment['changing_values'] + [entity.position]
    entity.direction = normalize_direction((entity.direction - 180))

def change_direction_REDUCE_VELOCITY(environment, entity):
    environment['changing_values'] = environment['changing_values'] + [entity.position]
    entity.current_velocity -= 1
    if entity.current_velocity < 0:
        entity.current_velocity = 0

def change_direction_INCREASE_VELOCITY(environment, entity):
    environment['changing_values'] = environment['changing_values'] + [entity.position]
    entity.current_velocity += 1
    if entity.current_velocity > entity.velocity:
        entity.current_velocity = entity.velocity