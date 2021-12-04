import numpy as np

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
def draw_plant():
    img = np.array([[1,0,0,0,0,0],
                    [1,1,0,0,0,1],
                    [0,1,1,0,1,0],
                    [0,0,1,1,0,0],
                    [0,0,0,1,0,0],
                    [0,0,0,1,0,0]])
    img = np.stack([img, img, img],axis=2)*255
    img = np.where(img>0,[0,255,0],0)
    return img
def draw_halt():
    img = np.array([[0,1,1,1,1,1],
                    [1,1,1,0,0,0],
                    [1,1,0,0,0,0],
                    [1,1,0,0,0,0],
                    [1,1,1,0,0,0],
                    [0,1,1,1,1,1]])
    img = np.stack([img, img, img],axis=2)*255
    img = np.where(img>0,[255,255,255],0)
    return img
def draw_hunt():
    img = np.array([[0,0,1,0,0,1],
                    [0,1,0,0,1,0],
                    [1,0,0,1,0,0],
                    [0,0,1,0,0,1],
                    [0,1,0,0,1,0],
                    [1,0,0,1,0,0]])
    img = np.stack([img, img, img],axis=2)*255
    img = np.where(img>0,[255,0,0],0)
    return img
def draw_changing_values():
    img = np.array([[1,1,1,1,1,1],
        [0,1,0,0,1,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,1,0,0,1,0],
        [1,1,1,1,1,1]])
    img = np.stack([img, img, img],axis=2)*255
    img = np.where(img>0,[0,255,255],0)
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
plant = draw_plant()
halt = draw_halt()
hunt = draw_hunt()
changing_values = draw_changing_values()

def draw_actions(environment=None, world=None, world_size=None):
    for x,y in environment['mate_interactions']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[x-3:x+3,y-3:y+3] = heart
        except:
            pass
        
    for x,y in environment['healing_interactions']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[x-3:x+3,y-3:y+3] = healing
        except:
            pass
        
    for x,y in environment['attack_interactions']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[x-3:x+3,y-3:y+3] = sword
        except:
            pass
    
    for x,y in environment['up']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[x-3:x+3,y-3:y+3] = up
        except:
            pass
    
    for x,y in environment['dn']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[x-3:x+3,y-3:y+3] = dn
        except:
            pass
    
    for x,y in environment['l']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[x-3:x+3,y-3:y+3] = l
        except:
            pass
        
    for x,y in environment['r']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = r
        except:
            pass
    
    for x,y in environment['upr']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = upr
        except:
            pass
        
    for x,y in environment['upl']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = upl
        except:
            pass
        
    for x,y in environment['dnr']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = dnr
        except:
            pass
        
    for x,y in environment['dnl']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = dnl
        except:
            pass
        
    for x,y in environment['random']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = rand
        except:
            pass
        
    for x,y in environment['forward']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = forward
        except:
            pass
        
    for x,y in environment['reverse']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = reverse
        except:
            pass
        
    for x,y in environment['plant']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = plant
        except:
            pass
        
    for x,y in environment['halt']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = halt
        except:
            pass
        
    for x,y in environment['hunt']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = hunt
        except:
            pass
        
    for x,y in environment['changing_values']:
        x += world_size[0][1]-8
        y += world_size[1][1]
        try:
            world[(x-3):(x+3),(y-3):(y+3)] = changing_values
        except:
            pass    