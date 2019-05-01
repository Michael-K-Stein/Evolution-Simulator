import pygame
from Evolution1.Generics import colors
import Evolution1.main

class Life:

    name = "Generic Life Form"
    x = 0
    y = 0
    color = "Blue"
    radius = 15

    Food = 0

    speed = 1

    def getLifeForms(self):
        return Evolution1.main.LifeForms
    def getFoodForms(self):
        return Evolution1.main.FoodForms

    def Birth(self, surface, name, x, y, color):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.surface = surface

        pygame.draw.circle(self.surface, colors[self.color],(x,y),self.radius)

    def Kill(self):
        self.x=0
        self.y=0
        self.color = "Brown"
        self.name = "Deceased (" + self.name +")"
        Evolution1.main.RemoveLife(self)

    def Move(self, toX, toY):
        print("Am at:",self.x,self.y,"Going to:",toX,toY)
        if abs(toX - self.x) > abs(toY - self.y):
            if abs(toX - self.x) > self.speed:
                if toX - self.x<0:
                    self.x -= self.speed
                else:
                    self.x += self.speed
            else:
                self.x = toX
        else:
            if abs(toY - self.y) > self.speed:
                if toY - self.y < 0:
                    self.y -= self.speed
                else:
                    self.y += self.speed
            else:
                self.y = toY

        pygame.draw.circle(self.surface, colors[self.color], (self.x, self.y), 15)

    def detectColissions(self):
        for foodForm in self.getFoodForms():
            if self.distanceTo(foodForm.x,foodForm.y) < foodForm.radius + self.radius:
                self.Food += foodForm.feed
                foodForm.remove()

    def distanceTo(self, x, y):
        return ((x - self.x)**2 + (y - self.y)**2)**0.5

    def locateClosestFood(self):
        FoodForms = self.getFoodForms()
        closest = FoodForms[0]
        closestVal = self.distanceTo(closest.x,closest.y)
        for foodForm in FoodForms:
            if self.distanceTo(foodForm.x,foodForm.y) < closestVal:
                closest = foodForm
                closestVal=self.distanceTo(foodForm.x,foodForm.y)
        return closest.x, closest.y