from scipy.spatial import distance
import math
import numpy as np

class Sensors:
    def __init__(self, entity, environment):
        self.Entity = entity
        self.environment = environment
        
    def __sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
        
    def velocity(self):
        return self.Entity.velocity/31
    
    def current_velocity(self):
        return self.Entity.current_velocity/self.Entity.velocity
    
    def direction(self):
        return self.Entity.direction/360
    
    def age(self):
        return (self.Entity.age)/100
    
    def size(self):
        return (self.Entity.size)/20
    
    def strength(self):
        return (self.Entity.strength)/100
    
    def health(self):
        return ((self.Entity.health)-100)/100
    
    def children(self):
        return (self.Entity.children)/10
    
    def food(self):
        return (self.Entity.food-100)/100
    
    def liked(self):
        return (self.Entity.liked)/100
    
    def energy(self):
        return (self.Entity.energy)/100
    
    def starving(self):
        return [1 if self.Entity.is_starving else -1][0]
    
    def mate(self):
        return [1 if self.Entity.can_mate else -1][0]
    
    
    def proximity_to_neighbor_XY(self):
        nodes = self.environment['all_entity_locations'][:]
        node = self.Entity.position
        nodes.remove(node)
        
        closest_node = nodes[distance.cdist([node], nodes).argmin()]
        
        x0, y0 = node
        x1, y1 = closest_node
        
        x = x0-x1
        y = y0-y1
        return x/1000, y/1000
    
    def direction_to_neighbor(self):
        nodes = self.environment['all_entity_locations'][:]
        node = self.Entity.position
        nodes.remove(node)
        
        closest_node = nodes[distance.cdist([node], nodes).argmin()]
        
        if closest_node == node:
            return
        
        x0, y0 = node
        x1, y1 = closest_node
        direction = math.degrees(math.atan2(int(y1-y0), int(x1-x0)))/360
        return direction
    
    def population_XY(self):
        nodes = self.environment['all_entity_locations'][:]
        node = self.Entity.position
        nodes.remove(node)
        
        nodes_arr = np.asarray(nodes)
        node_arr = np.asarray(node)
        
        x_density = (nodes_arr[:,0]>node_arr[0]).sum()/len(nodes_arr[:,0]) - (nodes_arr[:,0]<node_arr[0]).sum()/len(nodes_arr[:,0])
        y_density = (nodes_arr[:,1]>node_arr[1]).sum()/len(nodes_arr[:,1]) - (nodes_arr[:,1]<node_arr[1]).sum()/len(nodes_arr[:,1])
        return x_density, y_density
    
    def proximity_to_mate_XY(self): 
        if self.Entity.is_Male == True:
            nodes = self.environment['mate_female_positions'][:]
        else:
            nodes = self.environment['mate_male_positions'][:]
        node = self.Entity.position
        
        try:
            closest_node = nodes[distance.cdist([node], nodes).argmin()]
        except:
            return 0, 0
        
        x0, y0 = node
        x1, y1 = closest_node
        
        x = x0-x1
        y = y0-y1
        return x/1000, y/1000 # maybe replace with max world size
    
    # external identifiers
    ## Blockage x, y
    ## Proximity to next friend x, y
    ## Proximity to next enemy x, y
    ## Proximity to next plant x, y
    ## Proximity to next entity that can be mated x, y
    ## Proximity to next entity that can be fought x, y
    ## Proximity to world edge x, y