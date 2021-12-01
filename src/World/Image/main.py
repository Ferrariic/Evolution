import cv2
class GameWindow:
    def __init__(self, window_size_x, window_size_y):
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        
    def start(self):
        main_screen = [self.window_size_y, self.window_size_x, 3] = [0,0,0]
        cv2.imshow('Cataclysm-Evolution', main_screen)
        cv2.waitKey()
        
GameWindow(window_size_x=1920, window_size_y=1080).start()