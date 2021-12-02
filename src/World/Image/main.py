import cv2
import numpy as np
import random
import time

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
        self.page = None
        
    def __create_main_window(self):
        self.main_screen = np.zeros([self.window_height, self.window_width, 3], dtype=np.uint8)
        self.main_screen[:,:] = [0,0,0] # add main screen window here
        
    def __create_square(self, height=None, width=None, color=[255,255,255]):
        #BGR color scheme
        square = np.zeros([height, width, 3], dtype=np.uint8)
        square[:,:] = color
        return square
        
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
        
    def __draw_background(self):
        background = Build2D(shape = 256, threshold = 200, complexity=2, shift=.9).build_2d_square()
        background = np.stack([background, background, background], axis=2)
        channel_choice=0
        background[:,:,channel_choice] = background[:,:,channel_choice]/2
        background = background.astype(int)
        background = background.astype(np.uint8)
        return background
        
    def __draw_main_menu(self):
        # Background images
        
        singleplayer_box = self.__create_square(height=56, width=400, color=[255,255,255])
        multiplayer_box = self.__create_square(height=56, width=400, color=[255,255,255])
        level_builder_box = self.__create_square(height=56, width=400, color=[255,255,255])
        quit_box = self.__create_square(height=56, width=230, color=[255,255,255])
        options_box = self.__create_square(height=56, width=230, color=[255,255,255])
        music_box = self.__create_square(height=50, width=50, color=[255,255,255])
        
        self.__draw_object(singleplayer_box, center_on=self.main_screen, offset=(-80,0))
        self.__draw_object(multiplayer_box, center_on=self.main_screen, offset=(0,0))
        self.__draw_object(level_builder_box, center_on=self.main_screen, offset=(80,0))
        self.__draw_object(quit_box, center_on=self.main_screen, offset=(170,140))
        self.__draw_object(options_box, center_on=self.main_screen, offset=(170,-140))
        self.__draw_object(music_box, center_on=self.main_screen, offset=(250,400))
        
    def __draw_options(self):
        a_box = self.__create_square(height=56, width=400, color=[255,0,255])
        self.__draw_object(a_box, center_on=self.main_screen, offset=(-80,0))
    
    def detect_Mouse(self, event,x,y,flags,param):
        self.mouse_position = None
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.mouse_position = [x,y]
            print(self.mouse_position)

    def play(self):
        cv2.namedWindow('Cataclysm-Evolution')
        cv2.setMouseCallback('Cataclysm-Evolution', self.detect_Mouse)
        while True:
            self.__create_main_window()
            self.__draw_main_menu()
            cv2.imshow('Cataclysm-Evolution', self.main_screen)
            cv2.waitKey(delay=1)
        
DrawGame(window_height=600, window_width=900).play()