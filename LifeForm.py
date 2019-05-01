import pygame
from Evolution1.Generics import colors

class Life:

    name = "Generic Life Form"
    x = 0
    y = 0
    color = "Blue"

    Food = 0

    def Birth(self, surface, name, x, y, color):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.surface = surface

        pygame.draw.circle(self.surface, colors[self.color],(x,y),15)

    def Kill(self):
        self.x=0
        self.y=0
        self.color = "Black"
        self.name = "Deceased (" + self.name +")"

    def Move(self,toX, toY):
        x=toX
        y=toY