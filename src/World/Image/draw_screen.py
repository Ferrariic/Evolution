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
        images = self.environment['all_entity_images']
        sizes = self.environment['all_entity_sizes']
        
        zipped = list(zip(locations, images, sizes))
        
        self.world_information = []
        for coords, images, size in zipped:
            x = coords[0] + self.world_size[0][1]
            y = coords[1] + self.world_size[1][1]
            self.world_information.append([x, y, images, size])

            
    def draw_environment(self, environment, generation, year):
        def draw_heart():
            img = np.array([[0,1,0,0,1,0],
                            [1,1,1,1,1,1],
                            [0,1,1,1,1,0],
                            [0,1,1,1,1,0],
                            [0,1,1,1,1,0],
                            [0,0,1,1,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[255,0,0],0)
            return img
        def draw_sword():
            img = np.array([[0,0,1,1,0,0],
                            [0,0,1,1,0,0],
                            [0,0,1,1,0,0],
                            [1,1,1,1,1,1],
                            [0,0,1,1,0,0],
                            [0,0,1,1,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[255,255,0],0)
            return img
        def draw_healing():
            img = np.array([[0,0,1,1,0,0],
                            [0,0,1,1,0,0],
                            [1,1,1,1,1,1],
                            [1,1,1,1,1,1],
                            [0,0,1,1,0,0],
                            [0,0,1,1,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,0],0)
            return img
        def draw_up():
            img = np.array([[0,0,1,1,0,0],
                [0,1,1,1,1,0],
                [1,1,1,1,1,1],
                [0,0,1,1,0,0],
                [0,0,1,1,0,0],
                [0,0,1,1,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
            return img
        def draw_down():
            img = np.array([[0,0,1,1,0,0],
                [0,0,1,1,0,0],
                [0,0,1,1,0,0],
                [1,1,1,1,1,1],
                [0,1,1,1,1,0],
                [0,0,1,1,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
            return img
        def draw_left():
            img = np.array([[0,0,1,0,0,0],
                [0,1,1,0,0,0],
                [1,1,1,1,1,1],
                [1,1,1,1,1,1],
                [0,1,1,0,0,0],
                [0,0,1,0,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
        def draw_right():
            img = np.array([[0,0,0,1,0,0],
                [0,0,0,1,1,0],
                [1,1,1,1,1,1],
                [1,1,1,1,1,1],
                [0,0,0,1,1,0],
                [0,0,0,1,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
        
        self.__process_world_coordinates(environment=environment)
        x_max = abs(self.world_size[0][0]) + abs(self.world_size[0][1])
        y_max = abs(self.world_size[1][0]) + abs(self.world_size[1][1])
        world = np.zeros([x_max+5, y_max+5, 3], dtype=np.uint8)
        world[:,:] = [0,0,0]
        
        for x, y, image, size in self.world_information:
            image = np.array(image)
            try:
                world[x-(int(image.shape[0]/2)):x+int(image.shape[0]/2),
                      y-int(image.shape[1]/2):y+int(image.shape[1]/2)
                      ] = image
            except:
                pass
        
        for x,y in self.environment['mate_interactions']:
            x += self.world_size[0][1]-6
            y += self.world_size[1][1]
            try:
                world[x-3:x+3,y-3:y+3] = draw_heart()
            except:
                pass
            
        for x,y in self.environment['healing_interactions']:
            x += self.world_size[0][1]-6
            y += self.world_size[1][1]
            try:
                world[x-3:x+3,y-3:y+3] = draw_healing()
            except:
                pass
            
        for x,y in self.environment['attack_interactions']:
            x += self.world_size[0][1]-6
            y += self.world_size[1][1]
            try:
                world[x-3:x+3,y-3:y+3] = draw_sword()
            except:
                pass
        
        for x,y in self.environment['up']:
            x += self.world_size[0][1]-6
            y += self.world_size[1][1]
            try:
                world[x-3:x+3,y-3:y+3] = draw_up()
            except:
                pass
        
        for x,y in self.environment['dn']:
            x += self.world_size[0][1]-6
            y += self.world_size[1][1]
            try:
                world[x-3:x+3,y-3:y+3] = draw_down()
            except:
                pass
        
        for x,y in self.environment['l']:
            x += self.world_size[0][1]-6
            y += self.world_size[1][1]
            try:
                world[x-3:x+3,y-3:y+3] = draw_left()
            except:
                pass
            
        for x,y in self.environment['r']:
            x += self.world_size[0][1]-6
            y += self.world_size[1][1]
            print(x,y)
            world[(x-3):(x+3),(y-3):(y+3)] = draw_right()
            
        world = cv2.cvtColor(world, cv2.COLOR_BGR2RGB)
        world = cv2.putText(img=world, text=f'Generation: {generation} | Year: {year}', org=(10,500), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.4, thickness=1, color=(255,255,255))
        cv2.imshow('Cataclysm-Evolution', world)
        cv2.waitKey(delay=1)