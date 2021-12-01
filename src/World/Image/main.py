import cv2
import numpy as np

class DrawGame:
    
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
    
    def play(self):
        main_screen = np.zeros([self.window_height, self.window_width, 3], dtype=np.uint8)
        main_screen[:,:] = [0,0,0]
        
        cv2.imshow('Cataclysm-Evolution',main_screen)
        cv2.waitKey()
        
DrawGame(window_width=1280, window_height=720).play()