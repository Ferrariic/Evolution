import numpy as np
import cv2
from itertools import combinations
import random
import string
import time
import math
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from IPython import display
from scipy.spatial import distance


class WORLD:
    def __init__(self, starter_population=100, population_limit=1000, world_size=(400,500)):
        self.starter_population = starter_population
        self.world_size = world_size
        self.population_limit = population_limit 
        self.NPCs = None
        self.notable_food_locations = []
        self.male_mate_locations = []
        self.human_locations = []
        self.monster_locations = []
        self.doctor_locations = []
        self.female_mate_locations = []
        self.NPC_graveyard = []
        self.NPC_create
        self.video_images = []

    def create_starter_population(self):
        self.NPCs = [self.NPC_create().export_profile() for npc in range(self.starter_population)]

    def handle_interaction(self, NPC_interaction_list):
        def check_alive(NPC1, NPC2): # Checks to see if NPCs are alive before handling situation.
            if NPC1['is_Alive'] & NPC2['is_Alive']:
                return True
            return False

        def fight(NPC1, NPC2): # Fights NPCs
            if not check_alive(NPC1, NPC2):
                return
            NPC1['health'], NPC2['health'] = NPC1['health'] - NPC2['strength'], NPC2['health'] - NPC1['strength']
            NPC1['liked'], NPC2['liked'] = NPC1['liked'] - 2, NPC2['liked'] - 2

            if NPC1['health'] < 0:
                if NPC2['food'] >=0:
                    NPC1['food'] = NPC1['food']+NPC2['food'] # Takes their food
                    NPC1['is_Alive'] = False
                    NPC1['cause_of_death'] = 'Fighting'
                    NPC2['liked'] = NPC2['liked'] - 5

            if NPC2['health'] < 0:
                if NPC1['food'] >=0:
                    NPC2['food'] = NPC2['food']+NPC1['food'] # Takes their food
                    NPC2['is_Alive'] = False
                    NPC2['cause_of_death'] = 'Fighting'
                    NPC1['liked'] = NPC1['liked'] - 5
            
        def breed(NPC1, NPC2): # Breeds NPCs and creates new NPC on tile
            if not check_alive(NPC1, NPC2):
                return

            if (NPC1['children']<=10) and (NPC2['children']<=10): # if both have less than 5 kids in total
                NPC1['children'], NPC2['children'] = NPC1['children']+1, NPC2['children']+1
                NPC1['liked'], NPC2['liked'] = NPC1['liked']+1, NPC2['liked']+1
                NPC1['food'], NPC2['food'] = NPC1['food']-5, NPC2['food']-5

                # new baby
                new_NPC = self.NPC_create().export_profile()
                new_NPC['position'] = NPC1['position']
                
                new_NPC['job'] = random.choice([NPC1['job'], NPC2['job']])
                new_NPC['color'] = [int((NPC1['color'][0]+NPC2['color'][0])/2),int((NPC1['color'][1]+NPC2['color'][1])/2),int((NPC1['color'][2]+NPC2['color'][2])/2)]
                new_NPC['food'] = 0
                strengths = [NPC1['strength'],NPC2['strength']]
                velocities = [NPC1['velocity'],NPC2['velocity']]

                new_NPC['strength'] = random.randint(min(strengths), max(strengths))+random.randint(-5,5)
                if new_NPC['strength']<0:
                    new_NPC['strength']=0

                new_NPC['velocity'] = random.randint(min(velocities), max(velocities))
                new_NPC['will_Flee'] = random.choice([NPC1['will_Flee'], NPC2['will_Flee']])

                if new_NPC['job'] == 'hunter':
                    new_NPC['will_Flee'] = False
                    new_NPC['goal'] = 'hunt'

                self.NPCs.append(new_NPC)

        def give_extra_food(NPC1, NPC2):
            if (NPC1['food'] > NPC2['food']) & (NPC1['food'] > 0):
                if (NPC1['food'] > 10000):
                    NPC1['food'] = 10000
                    give_food = int(NPC1['food'])/2
                    NPC2['food'] = NPC2['food'] + give_food
                    NPC1['food'] = NPC1['food'] - give_food
                    NPC1['liked'] = NPC1['liked'] + give_food 
            if (NPC2['food'] > NPC1['food']) & (NPC2['food'] > 0):
                if (NPC2['food'] > 10000):
                    NPC2['food'] = 10000
                    give_food = int(NPC2['food'])/2
                    NPC1['food'] = NPC1['food'] + give_food
                    NPC2['food'] = NPC2['food'] - give_food
                    NPC2['liked'] = NPC2['liked'] + give_food 

        def help_elderly(NPC1, NPC2):
            if NPC1['age'] > NPC2['age']:
                NPC1['health'] = NPC1['health'] + 2
                NPC2['liked'] = NPC2['liked'] + 2
            if NPC2['age'] > NPC1['age']:
                NPC2['health'] = NPC2['health'] + 2
                NPC1['liked'] = NPC1['liked'] + 2

        def bury(NPC1, NPC2):
            if NPC1['is_Alive']:
                NPC1['liked'] = NPC1['liked']+1
            else:
                NPC2['liked'] = NPC2['liked']+1
            return
        
        def pick_plant(NPC1, NPC2):
            if NPC1['entity_type'] == 'human':
                NPC2['is_alive'] = False
                NPC2['cause_of_death'] = 'picked_by_human'
                NPC1['food'] += NPC2['food']
            if NPC2['entity_type'] == 'human':
                NPC1['is_alive'] = False
                NPC1['cause_of_death'] = 'picked_by_human'
                NPC2['food'] += NPC1['food']
        
        def heal_other(NPC1, NPC2):
            if (NPC1['job']=='doctor')&(NPC1['job_tasks']<200):
                NPC2['health'] = NPC2['health']+20
                NPC1['job_tasks'] = NPC1['job_tasks']+1
                NPC1['liked'] = NPC1['liked']+10
            if (NPC2['job']=='doctor')&(NPC2['job_tasks']<200):
                NPC1['health'] = NPC1['health']+20
                NPC2['job_tasks'] = NPC2['job_tasks']+1
                NPC2['liked'] = NPC2['liked']+10

        def hunt(NPC1, NPC2, hunting_modifier=2.5):
            if NPC1['job'] == 'hunter':
                NPC1['goal'] = 'hunt'
                NPC2['health'] -= NPC1['strength']*hunting_modifier
                if NPC2['health']<0:
                    NPC1['food'] += NPC2['food']
                    NPC1['liked'] += NPC2['health']
                    NPC2['is_Alive'] = False
                    NPC2['cause_of_death'] = 'Hunted by Human'
            if NPC2['job'] == 'hunter':
                NPC2['goal'] = 'hunt'
                NPC1['health'] -= NPC2['strength']*hunting_modifier
                if NPC1['health']<0:
                    NPC2['food'] += NPC1['food']
                    NPC2['liked'] += NPC1['health']
                    NPC1['is_Alive'] = False
                    NPC1['cause_of_death'] = 'Hunted by Human'

        def eat_human(NPC1, NPC2):
            if NPC1['entity_type'] == 'monster':
                NPC2['health'] -= NPC1['strength']
                if NPC2['health']<0:
                    NPC2['is_Alive'] = False
                    NPC2['cause_of_death'] = 'Eaten by Monster'

            if NPC2['entity_type'] == 'monster':
                NPC1['health'] -= NPC2['strength']
                if NPC1['health']<0:
                    NPC1['is_Alive'] = False
                    NPC1['cause_of_death'] = 'Eaten by Monster'

        for NPC_group in NPC_interaction_list: # Checks through interaction list for different conditions, if true executes condition.
            npc_combinations = combinations(NPC_group, 2)
            for NPC1, NPC2 in npc_combinations:
                """
                2x interactions
                """
                if (NPC1['is_Male'] & (NPC1['age']>12)) & (NPC2['is_Male'] & (NPC2['age']>12)) & (NPC1['liked']<5) & (NPC2['liked']<5):
                    fight(NPC1, NPC2)
                if (self.population_limit > len(self.human_locations))&(NPC1['entity_type']==NPC2['entity_type']=='human')&((((NPC1['is_Male'])&(NPC1['age']>18))&((~NPC2['is_Male'])&(NPC2['age']>18))) or (((~NPC1['is_Male'])&(NPC1['age']>18))&((NPC2['is_Male'])&(NPC2['age']>18)))) and ((NPC1['food']>0) & (NPC2['food']>0)):
                    breed(NPC1, NPC2)
                if ((NPC1['food'] > NPC2['food']) or (NPC2['food'] > NPC1['food']))&(NPC1['entity_type']==NPC2['entity_type']=='human'):
                    give_extra_food(NPC1, NPC2)
                if ((NPC1['age'] > NPC2['age']+15)&(NPC2['liked']>2)) or ((NPC2['age'] > NPC1['age']+15)&(NPC1['liked']>2)):
                    help_elderly(NPC1, NPC2)
                if NPC1['is_Alive'] != NPC2['is_Alive']:
                    bury(NPC1, NPC2)
                if ((NPC1['entity_type']=='plant')&(NPC1['age']>1)&(NPC2['age']>18)) or ((NPC2['entity_type']=='plant')&(NPC2['age']>1)&(NPC1['age']>18)):
                    pick_plant(NPC1, NPC2)
                if ((NPC1['job']=='doctor')&(NPC1['age']>18)) or ((NPC2['job']=='doctor')&(NPC2['age']>18)):
                    heal_other(NPC1, NPC2)
                if ((NPC1['job']=='hunter')&(NPC1['age']>18)&(NPC2['entity_type']=='monster')) or ((NPC2['job']=='hunter')&(NPC2['age']>18)&(NPC1['entity_type']=='monster')):
                    hunt(NPC1, NPC2)
                if ((NPC1['entity_type']=='monster')&(NPC1['age']>18)&(NPC2['entity_type']=='human')) or ((NPC2['entity_type']=='monster')&(NPC2['age']>18)&(NPC1['entity_type']=='human')):
                    eat_human(NPC1, NPC2)
        
    def generate_goal_points_of_interest(self):
        self.notable_food_locations = []
        self.male_mate_locations = []
        self.female_mate_locations = []
        self.human_locations = []
        self.monster_locations = []
        self.doctor_locations = []

        for NPC in self.NPCs:
            if NPC['entity_type'] == 'plant':
                self.notable_food_locations.append(NPC['position'])
            if (NPC['entity_type'] == 'human')&(NPC['is_Male']==True):
                self.male_mate_locations.append(NPC['position'])
            if (NPC['entity_type'] == 'human')&(NPC['is_Male']==False):
                self.female_mate_locations.append(NPC['position'])
            if (NPC['entity_type'] == 'human'):
                self.human_locations.append(NPC['position'])
            if (NPC['entity_type'] == 'monster'):
                self.monster_locations.append(NPC['position'])
            if (NPC['entity_type'] == 'human')&(NPC['job']=='doctor'):
                self.doctor_locations.append(NPC['position'])

    def set_goal(self):
        for NPC in self.NPCs:
            if (len(self.monster_locations) >0) & (NPC['job'] == 'hunter') & (NPC['age']>18):
                NPC['goal'] = 'hunt'
                continue
            if (NPC['food'] < 50): # NPC is starving
                NPC['goal'] = 'food'
                continue
            if (NPC['health'] < 50)&(NPC['entity_type']=='human'):
                NPC['goal'] = 'seek_medical'
                continue
            if (NPC['food'] > 100)&(NPC['age']>18)&(NPC['children']<=10)&(NPC['entity_type']=='human'):
                NPC['goal'] = 'mate'
                continue
            if (NPC['food'] > 200)&(NPC['entity_type']=='human'):
                NPC['goal'] = 'share_food'
                continue
            if (NPC['entity_type']=='monster'):
                NPC['goal'] = 'hunt_people'
                continue

    def check_interaction(self): # Produces an interaction list, and checks to see if NPCs are on top of eachother for interaction to be True.
        interactions = [tuple(NPC['position']) for NPC in self.NPCs]
        points_of_interest = list(set([interaction for interaction in interactions if interactions.count(interaction) > 1]))
        if len(points_of_interest) == 0:
            return
        name_interactions = [(i, x) for i, x in enumerate(interactions) for POI in points_of_interest if x == POI]
        interaction_idxs = {}
        for idx, pos in name_interactions:
            if pos in interaction_idxs:
                interaction_idxs[pos].append(idx)
            else:
                interaction_idxs[pos] = [idx]

        NPC_interaction_list = []
        for key, NPC_interactions in interaction_idxs.items():
            point_interaction = []
        for NPC_idx in NPC_interactions:
            NPC_data = self.NPCs[NPC_idx]
            point_interaction.append(NPC_data)
        NPC_interaction_list.append(point_interaction)
            
        self.handle_interaction(NPC_interaction_list)

    def do_jobs(self):
        """
        Yearly jobs
        """
        def plant(NPC):
            if (NPC['job_tasks']<=40): # number of years allowed to do task
                plant = self.NPC_create().export_profile()
                plant['entity_type'] = 'plant'
                plant['position'] = NPC['position']
                plant['velocity'] = 0
                plant['direction'] = 0
                plant['is_Alive'] = True
                plant['width'] = 3
                plant['strength'] = 0
                plant['will_Flee'] = False
                plant['color'] = [255,255,255]
                plant['health'] = random.randint(200,500)
                plant['food'] = random.randint(75,150)
                plant['liked'] = 0
                plant['job'] = None
                self.NPCs.append(plant)
                NPC['job_tasks'] = NPC['job_tasks']+1

        for NPC in self.NPCs:
            if len(self.notable_food_locations) < len(self.human_locations)*.5: # only plants double the number of humans on the field to prevent lag
                if NPC['job'] == 'farmer':
                    plant(NPC)

    def advance_age(self):
        for NPC in self.NPCs:
            # Adds one year to age
            NPC['age'] = NPC['age']+1

        # gives NPC a job when they get old enough
        if (NPC['age'] > 18) & (NPC['job'] is None) & (NPC['entity_type']=='human'):
            NPC['job'] = random.choice(['hunter','farmer','doctor'])#,'dummy'
            if NPC['job'] == 'hunter':
                NPC['will_Flee'] = False # prevents fleeing from monsters
                NPC['goal'] = 'hunt'

        #If starving remove health
        NPC['food'] -= 1
        if NPC['food'] <= 0:
            NPC['food'] = 0
            NPC['health'] -= 1
            if NPC['health']<0:
                NPC['is_Alive'] = False
                NPC['cause_of_death'] = 'Starvation'

        # Age decay
        if NPC['age']>120: 
            NPC['health'] -= (NPC['age']-120)*2
            NPC['strength'] -= (NPC['age']-120)*2
            if NPC['health']< 0:
                NPC['is_Alive'] = False
                NPC['cause_of_death'] = 'Old age'
            if (NPC['strength']<0)&(NPC['is_Alive']):
                NPC['strength']=0

        # food limit
        if NPC['food']>10000:
            NPC['food'] = 10000

        # plant decay
        start_plant_decay = 10
        if (NPC['entity_type'] == 'plant')&(NPC['age']>start_plant_decay):
            NPC['health'] -= (NPC['age']-start_plant_decay)
            if NPC['health']<0:
                NPC['is_Alive'] = False
                NPC['cause_of_death'] = 'Rotted away'

        # Cleanup dead
        if (NPC['is_Alive'] == False):
            self.NPCs.remove(NPC)
            self.NPC_graveyard.append(NPC)

    def release_monsters(self):
        monster_drop_table = random.randint(1,50)
        if monster_drop_table == 1:
            NPC = self.NPC_create().export_profile()
            NPC['entity_type'] = 'monster'
            NPC['health'] = random.randint(900, 1000)
            NPC['velocity'] = random.randint(1, 3)
            NPC['food'] = 5000
            NPC['width'] = 20
            NPC['will_Flee'] = False
            NPC['color'] = [255,0,0]
            NPC['goal'] = 'hunt_people'
            NPC['strength'] = random.randint(70,100)
            NPC['age'] = 0
            self.NPCs.append(NPC)
            return
        elif (monster_drop_table > 1)&(monster_drop_table < 25):
            NPC = self.NPC_create().export_profile()
            NPC['entity_type'] = 'monster'
            NPC['health'] = random.randint(100, 200)
            NPC['velocity'] = random.randint(20, 30)
            NPC['food'] = 2500
            NPC['width'] = 8
            NPC['will_Flee'] = False
            NPC['color'] = [255,0,0]
            NPC['goal'] = 'hunt_people'
            NPC['strength'] = random.randint(20,50)
            NPC['age'] = 0
            self.NPCs.append(NPC)
            return
        elif (monster_drop_table > 25):
            NPC = self.NPC_create().export_profile()
            NPC['entity_type'] = 'monster'
            NPC['health'] = random.randint(50, 100)
            NPC['velocity'] = random.randint(30, 50)
            NPC['food'] = 1000
            NPC['width'] = 6
            NPC['will_Flee'] = False
            NPC['color'] = [255,0,0]
            NPC['goal'] = 'hunt_people'
            NPC['strength'] = random.randint(5,10)
            NPC['age'] = 0
            self.NPCs.append(NPC)
            return

    def step(self, year):
        self.generate_goal_points_of_interest() # find points of interest
        self.set_goal() # set NPC goals to those points of interest
        self.calculate_new_position() # Calculates new positions for NPCs
        self.check_interaction() # Checks interaction listings
        self.do_jobs() # do jobs if jobs are assigned.
        self.advance_age() # Advances ages and cleans up field

        if year%10 == 0:
            self.release_monsters()

    def stats(self, year):
        x_list = []
        y_list = []
        draw_world = np.zeros([510,510,3],dtype=np.uint8)

        number_of_humans = 0
        number_of_plants = 0
        number_of_monsters = 0

        goal_food = 0
        goal_mate = 0
        goal_medical = 0
        goal_hunt = 0
        goal_share_food = 0

        num_doctors = 0
        num_hunters = 0
        num_farmers = 0
        num_dummy = 0

        count=0
        shift=0
        for NPC in self.NPCs:
            row, height = NPC['position'][0], NPC['position'][1]

            if NPC['entity_type'] == 'plant':
                draw_world[row:row+NPC['width']*2,height:height+NPC['width']] = NPC['color'] # tall plant
            elif NPC['job'] == 'hunter':
                draw_world[row:row+int(NPC['width']/2),height:height+NPC['width']] = NPC['color'] #Flat hunter shape
            else:
                draw_world[row:row+NPC['width'],height:height+NPC['width']] = NPC['color']

            if NPC['entity_type'] == 'human':
                length = 510
                if length-count-7 < 10:
                    count = 0
                    shift += 3
                    draw_world[485+shift:485+shift+2,5+count:5+count+2] = NPC['color']
                    count += 3

            if NPC['entity_type'] == 'human':
                number_of_humans += 1
            if NPC['entity_type'] == 'plant':
                number_of_plants += 1
            if NPC['entity_type'] == 'monster':
                number_of_monsters += 1
            if NPC['goal'] == 'food':
                goal_food += 1
            if NPC['goal'] == 'mate':
                goal_mate += 1
            if NPC['goal'] == 'seek_medical':
                goal_medical += 1
            if NPC['goal'] == 'share_food':
                goal_share_food += 1
            if NPC['goal'] == 'hunt':
                goal_hunt += 1
            if NPC['job'] == 'hunter':
                num_hunters += 1
            if NPC['job'] == 'doctor':
                num_doctors += 1
            if NPC['job'] == 'farmer':
                num_farmers += 1
            if NPC['job'] == 'dummy':
                num_dummy += 1

        text_year = f"Year: {year}"
        text_stats = f'Entities: Humans {number_of_humans}, Plants: {number_of_plants}, Monsters: {number_of_monsters}'
        text_goals = f'Goals: Find Food {goal_food}, Mate {goal_mate}, Hunt {goal_hunt}, Seek Medical {goal_medical}, Share {goal_share_food}'
        text_jobs = f'Jobs: Doctor {num_doctors}, Hunter {num_hunters}, Farmer {num_farmers}, Dummy {num_dummy}'
        
        print(text_year, text_stats, text_goals, text_jobs)
        draw_world = cv2.cvtColor(draw_world, cv2.COLOR_BGR2RGB)
        draw_world = cv2.putText(img=draw_world, text=text_year, org=(0,430), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.4, thickness=1, color=(255,255,255))
        draw_world = cv2.putText(img=draw_world, text=text_stats, org=(0,440), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.4, thickness=1, color=(255,255,255))
        draw_world = cv2.putText(img=draw_world, text=text_goals, org=(0,450), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.4, thickness=1, color=(255,255,255))
        draw_world = cv2.putText(img=draw_world, text=text_jobs, org=(0,460), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.4, thickness=1, color=(255,255,255))
        self.video_images.append(draw_world)
        # cv2.imshow('Cataclysm Evolution',draw_world)
        # plt.pause(0.05)

    def export(self):
        return self.NPC_graveyard + self.NPCs

    def export_video_images(self):
        return self.video_images

    def run_world(self):
        self.create_starter_population()
        for year in range(1000):
            self.step(year)
            self.stats(year)
            if len(self.human_locations) == 0:
                return

w = WORLD(starter_population=50, population_limit=200)
w.run_world()

import math

class Pathfinding:
    def __init__(self, Entity):
        self.Entity = Entity
    
    def calculate_new_position(self): # Calculates the new position of the NPC and makes sure the bounds are correct.
        def closest_node(node, nodes):
            closest_index = distance.cdist([node], nodes).argmin()
            return nodes[closest_index]

        def is_out_of_bounds(x1, y1):
            if x1 < 0 or x1 > self.world_size[0] or y1 < 0 or y1 > self.world_size[1]:
                return True
            return False

        def walk_to_goal(goal, NPC):
            x1,y1 = goal[0], goal[1]
            x0,y0 = NPC['position'][0], NPC['position'][1] 
            vel = NPC['velocity']
            direction = math.atan2(int(y1-y0), int(x1-x0))

            # if displacement is less than velocity, set destination to target.
            displacement = abs((((x0-x1)**2)+((y0-y1)**2))**(1/2))
            if displacement < vel: 
                xN1 = x1
                yN1 = y1
            else:
                xN1 = int(x0)+int(math.cos(direction)*vel)
                yN1 = int(y0)+int(math.sin(direction)*vel)
            if is_out_of_bounds(xN1, yN1):
                xN1, yN1 = x0, y0
            NPC['position'] = [xN1, yN1]
            NPC['direction'] = direction
            return

        def flee_from_monster(goal, NPC):
            x1, y1 = goal[0], goal[1] # monster position
            x0, y0 = NPC['position'][0], NPC['position'][1] 
            vel = NPC['velocity']

            direction = math.atan2(int(y1-y0), int(x1-x0))
            displacement = abs((((x0-x1)**2)+((y0-y1)**2))**(1/2))
            if displacement < vel*3:
                xN1 = int(x0)+int(math.cos(-direction)*abs(velocity))
                yN1 = int(y0)+int(math.sin(-direction)*abs(velocity))
                if is_out_of_bounds(xN1, yN1):
                    xN1, yN1 = x0, y0
                    NPC['position'] = [xN1, yN1]
                    NPC['direction'] = direction
                    return True
                return False

        for NPC in self.NPCs:
            x0 = NPC['position'][0]
            y0 = NPC['position'][1]
            direction = NPC['direction']
            velocity = NPC['velocity']

            # if NPC goal is food
            if NPC['goal'] == 'food':
                if len(self.notable_food_locations) > 0:
                    goal = closest_node(NPC['position'],self.notable_food_locations)
                    walk_to_goal(goal, NPC)
                    continue

            # if npc will flee from threats
            if NPC['will_Flee']:
                if len(self.monster_locations) > 0:
                    goal = closest_node(NPC['position'],self.monster_locations)
                    if flee_from_monster(goal, NPC):
                        continue
                    continue

            # if NPC is weak find doctor:
            if NPC['goal'] == 'seek_medical':
                if len(self.doctor_locations)>0:
                    goal = closest_node(NPC['position'],self.doctor_locations)
                    walk_to_goal(goal, NPC)
                    continue

            # if npc goal is to mate & is female
            if (NPC['goal']=='mate')&(NPC['age']>18)&(NPC['is_Male']==False)&(NPC['entity_type']=='human'):
                if len(self.male_mate_locations) > 0:
                    goal = closest_node(NPC['position'],self.male_mate_locations)
                    walk_to_goal(goal, NPC)
                    continue

            # goal to mate and is male
            if (NPC['goal']=='mate')&(NPC['age']>18)&(NPC['is_Male']==True)&(NPC['entity_type']=='human'):
                if len(self.female_mate_locations) > 0:
                    goal = closest_node(NPC['position'], self.female_mate_locations)
                    walk_to_goal(goal, NPC)
                    continue

            # goal is to hunt people
            if (NPC['goal']=='hunt_people'):
                if len(self.human_locations) > 0:
                    goal = closest_node(NPC['position'],self.human_locations)
                    walk_to_goal(goal, NPC)
                    continue

            # goal is to hunt monsters
            if (NPC['goal']=='hunt')&(NPC['age']>18):
                if len(self.monster_locations) > 0:
                    goal = closest_node(NPC['position'],self.monster_locations)
                    walk_to_goal(goal, NPC)
                    continue

            # goal is to share food
            if (NPC['goal']=='share_food'):
                if len(self.human_locations) > 0:
                    goal = closest_node(NPC['position'],self.human_locations)
                    walk_to_goal(goal, NPC)
                    continue

            # Random walk
            if NPC['goal'] == None:
                x1 = int(x0)+int(math.cos(math.radians(direction))*velocity)
                y1 = int(y0)+int(math.sin(math.radians(direction))*velocity)
                if is_out_of_bounds(x1, y1): # if out of bounds reset bounds
                    x1, y1 = x0, y0
                    direction = direction*random.choice([1,-1])*random.random()
                    velocity = velocity*random.choice([1,-1])*random.random()
                    NPC['position'] = [x1, y1]
                    NPC['direction'] = direction