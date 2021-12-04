import numpy as np
from .icons import *

def draw(item=None, color=None):
    item = np.stack([item, item, item], axis=2)*255
    item = np.where(item>0, color, 0)
    return item

sword = draw(item=sword_img, color=sword_colors)
heart = draw(item=heart_img, color=heart_colors)
healing = draw(item=healing_img, color=healing_colors)
up = draw(item=up_img, color=up_colors)
dn = draw(item=dn_img, color=dn_colors)
l = draw(item=l_img, color=l_colors)
r = draw(item=r_img, color=r_colors)
upr = draw(item=upr_img, color=upr_colors)
upl = draw(item=upl_img, color=upl_colors)
dnr = draw(item=dnr_img, color=dnr_colors)
dnl = draw(item=dnl_img, color=dnl_colors)
rand = draw(item=random_img, color=random_colors)
forward = draw(item=forward_img, color=forward_colors)
reverse = draw(item=reverse_img, color=reverse_colors)
plant = draw(item=plant_img, color=plant_colors)
halt = draw(item=halt_img, color=halt_colors)
hunt = draw(item=hunt_img, color=halt_colors)
changing_values = draw(item=changing_values_img, color=changing_values_colors)

draw_dict = {
            'mate_interactions':heart,
            'healing_interactions':healing,
            'attack_interactions':sword,
            'up':up,
            'dn':dn,
            'l':l,
            'r':r,
            'upr':upr,
            'upl':upl,
            'dnr':dnr,
            'dnl':dnl,
            'random':rand,
            'forward':forward,
            'reverse':reverse,
            'plant':plant,
            'halt':halt,
            'hunt':hunt,
            'changing_values':changing_values,
            }

def draw_actions(environment=None, world=None, world_size=None):
    for key, value in draw_dict.items():
        for x,y in environment[key]:
            x += world_size[0][1]-8
            y += world_size[1][1]
            try:
                world[(x-3):(x+3),(y-3):(y+3)] = value
            except:
                pass    