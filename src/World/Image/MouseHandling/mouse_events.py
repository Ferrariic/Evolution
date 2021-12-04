import numpy as np
from scipy.spatial import distance
import cv2

class MouseEvents:
    def __init__(self, mouseposition, environment, world, world_size):
        self.mouseposition = mouseposition
        self.environment = environment
        self.world = world
        self.world_size = world_size
        
    def __draw_mouse_box(self):
        img = np.array([[1,1,1,1,1,1],
                        [1,0,0,0,0,1],
                        [1,0,0,0,0,1],
                        [1,0,0,0,0,1],
                        [1,0,0,0,0,1],
                        [1,1,1,1,1,1]])
        img = np.stack([img, img, img],axis=2)*255
        img = np.where(img>0,[0,255,0],0)
        return img
    
    def __draw_entity_bounding_box(self):
        img = np.array([[1,1,1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1],
                        [1,1,1,1,1,1,1,1,1,1],])
        img = np.stack([img, img, img],axis=2)*255
        img = np.where(img>0,[255,255,0],0)
        return img
                
    def __mark_mouse_position(self):
        '''mark mouse position'''
        x = self.mouseposition[1]
        y = self.mouseposition[0]
        try:
            self.world[x-3:x+3,y-3:y+3] = self.__draw_mouse_box()
        except:
            print("Mouse out of bounds.")
            pass
        
    def __draw_box_around_closest_entity(self):
        x = self.mouseposition[1] - self.world_size[0][1]
        y = self.mouseposition[0] - self.world_size[1][1]
        
        node = [x,y]
        nodes = self.environment['all_entity_locations'][:]
        
        try:
            nodes.remove(node)
        except:
            pass
        
        '''finding closest entity to cursor'''
        closest_node = nodes[distance.cdist([node], nodes).argmin()]
        closest_node_index = self.environment['all_entity_locations'].index(closest_node)
        entity = self.environment['environment_json'][closest_node_index]
        
        '''drawing to screen'''
        x1, y1 = closest_node
        world_x = x1 + self.world_size[1][0] # world position conversions
        world_y = y1 + self.world_size[1][1] # world position conversions
        try:
            bounding_box = self.__draw_entity_bounding_box()
            bounding_box.astype('uint8')
            world_range = self.world[world_x-10:world_x,world_y-5:world_y+5]
            world_overlay = np.where(bounding_box>0, bounding_box, world_range)
            self.world[world_x-8:world_x+2,world_y-5:world_y+5] = world_overlay
        except:
            pass
        
        name = entity['name']
        genome_length = len(entity['genome'].split(' '))
        genome_header = entity['genome'].split(' ')[0]
        health = int(entity['health'])
        food = int(entity['food'])
        strength = int(entity['strength'])
        age = int(entity['age'])
        energy = int(entity['energy'])
        
        text = f'{name} {genome_header} H:{health} A:{age} S:{strength} E:{energy} F:{food} G:{genome_length}'
        try:
            self.world = cv2.putText(img=self.world, text=text, org=(10,485), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.4, thickness=1, color=(255,255,255))
        except:
            pass
        
        
    def process_events(self):
        self.__mark_mouse_position()
        self.__draw_box_around_closest_entity()
        return self.world
    
    