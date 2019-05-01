import pygame,random,math
class WorldSim():
    def __init__(self,w,h):
        pygame.init()
        screen_width, screen_height = (w,h)
        self.surface = pygame.display.set_mode((screen_width,screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Life Simulator")