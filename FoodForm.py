import pygame
from Evolution1.Generics import colors

class Food:

    name = "Generic Life Form"
    x = 0
    y = 0
    color = colors["yellow"]

    Food = 0

    def Grow(self, surface, x, y, type):
        self.x = x
        self.y = y
        self.surface = surface

        pygame.draw.circle(self.surface, self.color,(x,y),5)
