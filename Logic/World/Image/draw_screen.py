import cv2
import numpy as np

class DrawImage:
    
    def __init__(self, world_size):
        self.environment = None
        self.world_size = world_size
        self.world_information = None
        
    def __process_world_coordinates(self, environment):
        self.environment = environment
        locations = self.environment['all_entity_locations']
        colors = self.environment['all_entity_colors']
        
        zipped = list(zip(locations, colors))
        
        self.world_information = []
        for coords, color in zipped:
            x = coords[0] + self.world_size[0][1]
            y = coords[1] + self.world_size[1][1]
            self.world_information.append([x,y,color])

            
    def draw_environment(self, environment):
        self.__process_world_coordinates(environment=environment)
        x_max = abs(self.world_size[0][0]) + abs(self.world_size[0][1])
        y_max = abs(self.world_size[1][0]) + abs(self.world_size[1][1])
        world = np.zeros([x_max+5, y_max+5, 3], dtype=np.uint8)
        world[:,:] = [0,0,0]
        
        for x, y, color in self.world_information:
            world[x:x+5,y:y+5] = color
        cv2.imshow('world', world)
        cv2.waitKey(delay=1)