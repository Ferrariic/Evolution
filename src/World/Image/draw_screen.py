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

            
    def draw_environment(self, environment, generation, year, actions=True):
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
            return img
        def draw_right():
            img = np.array([[0,0,0,1,0,0],
                            [0,0,0,1,1,0],
                            [1,1,1,1,1,1],
                            [1,1,1,1,1,1],
                            [0,0,0,1,1,0],
                            [0,0,0,1,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
            return img
        def draw_up_right():
            img = np.array([[0,0,1,1,1,1],
                            [0,0,0,1,1,1],
                            [0,0,1,1,1,1],
                            [0,1,1,1,0,1],
                            [1,1,1,0,0,0],
                            [1,1,0,0,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
            return img
        def draw_up_left():
            img = np.array([[1,1,1,1,0,0],
                            [1,1,1,0,0,0],
                            [1,1,1,1,0,0],
                            [1,0,1,1,1,0],
                            [0,0,0,1,1,1],
                            [0,0,0,0,1,1],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
            return img
        def draw_dn_right():
            img = np.array([[1,1,0,0,0,0],
                            [1,1,1,0,0,0],
                            [0,1,1,1,0,1],
                            [0,0,1,1,1,1],
                            [0,0,0,1,1,1],
                            [0,0,1,1,1,1],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
            return img
        def draw_dn_left():
            img = np.array([[0,0,0,0,1,1],
                            [0,0,0,1,1,1],
                            [1,0,1,1,1,0],
                            [1,1,1,1,0,0],
                            [1,1,1,0,0,0],
                            [1,1,1,1,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,255],0)
            return img
        def random_walk():
            img = np.array([[0,1,1,1,1,0],
                            [1,0,0,0,0,1],
                            [1,0,0,0,1,0],
                            [0,0,1,1,0,0],
                            [0,0,1,0,0,0],
                            [0,0,1,0,0,0],])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[255,0,255],0)
            return img
        def draw_forward():
            img = np.array([[1,1,1,1,1,0],
                            [1,0,0,0,0,0],
                            [1,1,1,1,0,0],
                            [1,0,0,0,0,0],
                            [1,0,0,0,0,0],
                            [1,0,0,0,0,0]])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[0,255,0],0)
            return img
        def draw_reverse():
            img = np.array([[1,1,1,1,1,1],
                            [1,0,0,0,0,1],
                            [1,1,1,1,1,1],
                            [1,0,0,1,0,0],
                            [1,0,0,0,1,0],
                            [1,0,0,0,0,1]])
            img = np.stack([img, img, img],axis=2)*255
            img = np.where(img>0,[255,0,0],0)
            return img
                    
        sword = draw_sword()
        heart = draw_heart()
        healing = draw_healing()
        up = draw_up()
        dn = draw_down()
        l = draw_left()
        r = draw_right()
        upr = draw_up_right()
        upl = draw_up_left()
        dnr = draw_dn_right()
        dnl = draw_dn_left()
        rand = random_walk()
        forward = draw_forward()
        reverse = draw_reverse()
        
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
        
        if actions:
            for x,y in self.environment['mate_interactions']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[x-3:x+3,y-3:y+3] = heart
                except:
                    pass
                
            for x,y in self.environment['healing_interactions']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[x-3:x+3,y-3:y+3] = healing
                except:
                    pass
                
            for x,y in self.environment['attack_interactions']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[x-3:x+3,y-3:y+3] = sword
                except:
                    pass
            
            for x,y in self.environment['up']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[x-3:x+3,y-3:y+3] = up
                except:
                    pass
            
            for x,y in self.environment['dn']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[x-3:x+3,y-3:y+3] = dn
                except:
                    pass
            
            for x,y in self.environment['l']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[x-3:x+3,y-3:y+3] = l
                except:
                    pass
                
            for x,y in self.environment['r']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[(x-3):(x+3),(y-3):(y+3)] = r
                except:
                    pass
            
            for x,y in self.environment['upr']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[(x-3):(x+3),(y-3):(y+3)] = upr
                except:
                    pass
                
            for x,y in self.environment['upl']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[(x-3):(x+3),(y-3):(y+3)] = upl
                except:
                    pass
                
            for x,y in self.environment['dnr']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[(x-3):(x+3),(y-3):(y+3)] = dnr
                except:
                    pass
                
            for x,y in self.environment['dnl']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[(x-3):(x+3),(y-3):(y+3)] = dnl
                except:
                    pass
                
            for x,y in self.environment['random']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[(x-3):(x+3),(y-3):(y+3)] = rand
                except:
                    pass
                
            for x,y in self.environment['forward']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[(x-3):(x+3),(y-3):(y+3)] = forward
                except:
                    pass
                
            for x,y in self.environment['reverse']:
                x += self.world_size[0][1]-8
                y += self.world_size[1][1]
                try:
                    world[(x-3):(x+3),(y-3):(y+3)] = reverse
                except:
                    pass
                
                
        world = cv2.cvtColor(world, cv2.COLOR_BGR2RGB)
        world = cv2.putText(img=world, text=f'Generation: {generation} | Year: {year}', org=(10,500), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.4, thickness=1, color=(255,255,255))
        cv2.imshow('Cataclysm-Evolution', world)
        cv2.waitKey(delay=1)