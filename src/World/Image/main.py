import cv2
import numpy as np
import random
import time
from PIL import Image
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from numpy.core.defchararray import center

class Build2D:
    def __init__(self, seed=(int(time.time())), shape=4, threshold=100, complexity=1, shift=1):
        self.seed = seed
        if self.seed is not None:
            np.random.seed(self.seed)

        self.shape = shape # The shape of the starter square
        self.threshold = threshold # The threshold to remove pixels, 0-255. Higher removing more pixels.
        self.complexity = complexity # How many times the pattern is to be repeated
        self.shift = shift # How to shift the original triangle being replicated
        self.arr = None

    def __build_triangle(self):
        # Builds starter triangle pattern by forming a random square
        self.arr = np.random.rand(self.shape, self.shape)
        self.arr = self.arr*255
        
        # reflects square across xy axis, flips the triangle pattern onto the other side
        for row, rows in enumerate(self.arr):
            for column, column_value in enumerate(rows):
                if row > column:
                    self.arr[column, row] = self.arr[row, column]*self.shift

    def __build_square(self):
        self.shape = self.arr.shape[0]
        master_tile = np.zeros([self.shape*2, self.shape*2])
        for i in range(0, 4):
            tile = np.rot90(self.arr, k=2) # rotates the tile
            master_tile[0:self.shape,0:self.shape] = tile # sets the tile in place in the master tile
            master_tile = np.rot90(master_tile, k=1) # rotates the master tile
        self.arr = master_tile

    def build_2d_square(self):
        self.__build_triangle()
        for i in range(self.complexity):
            self.__build_square()
        return self.arr
    
class DrawGame:
    
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.main_screen = None
        self.object_positions = dict()
        self.mouse_position = None
        self.time_seed = int(time.time())
        self.page = None
        
    '''flushes window'''
    def __create_main_window(self):
        self.main_screen = np.zeros([self.window_height, self.window_width, 3], dtype=np.uint8)
        self.main_screen[:,:] = [0,0,0] # add main screen window here
        
    '''displays screen, converts BGR to RGB'''
    def __display_screen(self):
        self.main_screen = cv2.cvtColor(self.main_screen, cv2.COLOR_BGR2RGB)
        cv2.imshow('Cataclysm-Evolution', self.main_screen)
        cv2.waitKey(delay=1)
        
    """
        Objects
    """
    def __create_square(self, height=None, width=None, cmap_color='bone', intensity=1):
        #BGR color scheme
        np.random.seed(self.time_seed) # prevents
        square = np.random.rand(height,width)
        cmap = cm.get_cmap(cmap_color, 20)
        square = (cmap(square[:,:])*255)*intensity
        square = square[:,:,0:3]
        
        square = square.astype(int)
        square = square.astype(np.uint8)
        return square
        
        """
            Drawing an object
        """
    def __draw_object(self, img, center_on=None, offset=None):
        if img.shape[0] > center_on.shape[0]:
            img = img[0:center_on.shape[0],:]
        if img.shape[1] > center_on.shape[1]:
            img =  img[:,0:center_on.shape[1]]
        
        height_mid = int(center_on.shape[0]/2)
        width_mid = int(center_on.shape[1]/2)
        
        img_hmid = int(img.shape[0]/2)
        img_wmid = int(img.shape[1]/2)
        
        h_off = offset[0]
        w_off = offset[1]
        
        self.main_screen[
            (height_mid-img_hmid+h_off):(height_mid+img_hmid+h_off),
            (width_mid-img_wmid+w_off):(width_mid+img_wmid+w_off)
        ] = img
        
    '''depr draw random 2d background and place, it's kind of ugly'''
    def __draw_background(self):
        background = Build2D(shape = 256, threshold = 0, complexity=1, shift=.9).build_2d_square()
        background = np.stack([background, background, background], axis=2)
        channel_choice=0
        background[:,:,channel_choice] = background[:,:,channel_choice]/2
        background = background.astype(int)
        background = background.astype(np.uint8)
        background = cv2.resize(background, (900,600))
        return background
        
    """
        Pages        
    """
    '''Main Menu'''
    def __draw_main_menu(self):
        self.__create_main_window() # Flushes screen
        
        # Background images
        
        '''singleplayer box'''
        singleplayer_box_background = self.__create_square(height=56, width=400,cmap_color='summer_r',intensity=.75)
        singleplayer_box = self.__create_square(height=46, width=388, cmap_color='summer')
        
        self.__draw_object(singleplayer_box_background, center_on=self.main_screen, offset=(-80,0))
        self.__draw_object(singleplayer_box, center_on=self.main_screen, offset=(-80,0))
        
        '''multiplayer box'''
        multiplayer_box_background = self.__create_square(height=56, width=400,cmap_color='inferno_r',intensity=.75)
        multiplayer_box = self.__create_square(height=46, width=388,cmap_color='inferno')
        
        self.__draw_object(multiplayer_box_background, center_on=self.main_screen, offset=(0,0))
        self.__draw_object(multiplayer_box, center_on=self.main_screen, offset=(0,0))
        
        '''level builder box'''
        levelbuilder_box_background = self.__create_square(height=56, width=400,cmap_color='winter_r',intensity=.75)
        levelbuilder_box = self.__create_square(height=46, width=388,cmap_color='winter')
        
        self.__draw_object(levelbuilder_box_background, center_on=self.main_screen, offset=(80,0))
        self.__draw_object(levelbuilder_box, center_on=self.main_screen, offset=(80,0))
        
        '''quit box'''
        quit_box_background = self.__create_square(height=56, width=230,cmap_color='bone_r',intensity=.75)
        quit_box = self.__create_square(height=46, width=218,cmap_color='bone')
        
        self.__draw_object(quit_box_background, center_on=self.main_screen, offset=(170,140))
        self.__draw_object(quit_box, center_on=self.main_screen, offset=(170,140))
        
        '''options box'''
        options_box_background = self.__create_square(height=56, width=230,cmap_color='spring_r',intensity=.75)
        options_box = self.__create_square(height=46, width=218,cmap_color='spring')
        
        self.__draw_object(options_box_background, center_on=self.main_screen, offset=(170,-140))
        self.__draw_object(options_box, center_on=self.main_screen, offset=(170,-140))
        
        '''music box'''
        music_box_background = self.__create_square(height=50, width=50,cmap_color='ocean_r',intensity=.75)
        music_box = self.__create_square(height=38, width=38,cmap_color='ocean')
        
        self.__draw_object(music_box_background, center_on=self.main_screen, offset=(250,400))
        self.__draw_object(music_box, center_on=self.main_screen, offset=(250,400))
    
    '''detects mouse events'''
    def detect_Mouse(self, event,x,y,flags,param):
        self.mouse_position = None
        if (event == cv2.EVENT_LBUTTONDOWN) or (event == cv2.EVENT_LBUTTONDBLCLK):
            self.mouse_position = [x,y]

    def play(self):
        cv2.namedWindow('Cataclysm-Evolution')
        cv2.setMouseCallback('Cataclysm-Evolution', self.detect_Mouse)
        page = 'Main_menu'
        while True:
            if page =='Main_menu':
                self.__draw_main_menu()
                #print(self.mouse_position)
            self.__display_screen()
        
DrawGame(window_height=600, window_width=900).play()