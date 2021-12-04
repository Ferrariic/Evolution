import cv2
import numpy as np
from .Assets import assets
from .MouseHandling import mouse_events

class DrawImage:
    
    def __init__(self, world_size):
        self.environment = None
        self.world_size = world_size
        self.world_information = None
        self.mouse_position = None
        cv2.namedWindow('Cataclysm-Evolution')
        cv2.setMouseCallback('Cataclysm-Evolution', self.detect_Mouse)
        
    def detect_Mouse(self, event,x,y,flags,param):
        if (event == cv2.EVENT_LBUTTONDOWN) or (event == cv2.EVENT_LBUTTONDBLCLK):
            self.mouse_position = [x,y]
        
    def __process_world_coordinates(self, environment):
        self.environment = environment
        locations = self.environment['all_entity_locations']
        images = self.environment['all_entity_images']
        sizes = self.environment['all_entity_sizes']
        
        zipped = list(zip(locations, images, sizes))
        
        self.world_information = []
        for coords, images, size in zipped:
            x = coords[0] + self.world_size[0][1]
            y = coords[1] + self.world_size[1][1]
            self.world_information.append([x, y, images, size])
            
    def draw_environment(self, environment, generation, year, actions=True):
        '''draw world canvas'''
        self.__process_world_coordinates(environment=environment)
        x_max = abs(self.world_size[0][0]) + abs(self.world_size[0][1])
        y_max = abs(self.world_size[1][0]) + abs(self.world_size[1][1])
        world = np.zeros([x_max+5, y_max+5, 3], dtype=np.uint8) # makes blank world
        world[:,:] = [0,0,0] #sets background to zero
        
        '''draws sprites on world'''
        for x, y, image, size in self.world_information:
            image = np.array(image)
            try:
                world[x-(int(image.shape[0]/2)):x+int(image.shape[0]/2),
                      y-int(image.shape[1]/2):y+int(image.shape[1]/2)
                      ] = image
            except:
                pass
        
        '''draws actions of sprites'''
        if actions:
            assets.draw_actions(environment=self.environment, world=world, world_size=self.world_size)
        
        '''draws mouse events'''
        if self.mouse_position is not None:
            world = mouse_events.MouseEvents(mouseposition=self.mouse_position, environment=self.environment, world=world, world_size=self.world_size).process_events()
        
        '''writes world text as overlay'''
        world = cv2.cvtColor(world, cv2.COLOR_BGR2RGB)
        world = cv2.putText(img=world, text=f'Generation: {generation} | Year: {year}', org=(10,500), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.4, thickness=1, color=(255,255,255))
        cv2.imshow('Cataclysm-Evolution', world)
        cv2.waitKey(delay=1)