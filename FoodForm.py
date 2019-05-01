import pygame
from Evolution1.Generics import colors
import Evolution1.main
from Evolution1.main import FoodForms

class Food:

    name = "Generic Food Form"
    x = 0
    y = 0
    color = colors["yellow"]
    radius = 5

    feed = 1

    def Grow(self, surface, x, y, type):
        self.x = x
        self.y = y
        self.surface = surface

        pygame.draw.circle(self.surface, self.color,(x,y),self.radius)

    def remove(self):
        Evolution1.main.RemoveFood(self)