import math
import random
import pygame
from pygame import Color
from Evolution1.Generics import colors
from Evolution1.Graphics import WorldSim
#from Evolution1.LifeForm import Life
#from Evolution1.FoodForm import Food


class Food:

    name = "Generic Food Form"
    x = 0
    y = 0
    color = "yellow"
    radius = 5

    feed = 1

    def Grow(self, surface, x, y, type):
        self.x = x
        self.y = y
        self.surface = surface

    def Remove(self):
        self.color = colors["brown"]
        RemoveFood(self)

class Life:

    name = "Generic Life Form"
    x = 0
    y = 0
    color = "Blue"
    radius = 15

    Food = 0

    ini_speed = 1
    speed = 1

    def getLifeForms(self):
        return LifeForms
    def getFoodForms(self):
        return FoodForms

    def Birth(self, surface, name, x, y, color):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.surface = surface


    def Kill(self):
        self.x=0
        self.y=0
        self.color = "Brown"
        self.name = "Deceased (" + self.name +")"
        RemoveLife(self)

    def Move(self, toX, toY):
        #print("Am at:",self.x,self.y,"Going to:",toX,toY)
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

    def detectColissions(self):
        for foodForm in self.getFoodForms():
            #print("Distance",self.distanceTo(foodForm.x,foodForm.y))
            if self.distanceTo(foodForm.x,foodForm.y) < foodForm.radius + self.radius:
                self.eat(foodForm.feed)
                foodForm.Remove()

    def distanceTo(self, x, y):
        print(self.x,self.y,x,y,"",((x - self.x)**2 + (y - self.y)**2)**0.5)
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

    def eat(self, food):
        self.Food += food
        if self.Food > 10:
            self.speed = int(self.ini_speed * ((self.Food / 10)**0.5))
        else:
            self.speed = self.ini_speed

def randomChance(d): # Boolean with a chance of 1/d of giving True
    rndNum = random.random()
    if rndNum <= 1/d:
        return True
    else:
        return False

def RemoveFood(foodForm):
    FoodForms.remove(foodForm)
def RemoveLife(lifeForm):
    LifeForms.remove(lifeForm)

print("Starting World")

# Definitions

speed = 2
width = 800
height = 600

#

world = WorldSim(width,height)
surface = world.surface
clock = world.clock

a = 0

def CreateLife():
    if randomChance(2):
        newLife = Life()
        x, y = random.randint(0, width), random.randint(0, height)
        newLife.Birth(surface, "Gen" + str(a), x, y, "red")
        LifeForms.append(newLife)
        print("Created: ", "Gen" + str(a), x, y)
def GrowFood():
    if randomChance(2):
        newFood = Food()
        x, y = random.randint(0, width), random.randint(0, height)
        newFood.Grow(surface, x, y, 1)
        FoodForms.append(newFood)
        print("Created: ", "Food", x, y)

font = pygame.font.SysFont('Ubuntu',20,True)
def drawText(surface, message, pos, color=(255, 255, 255)):
    surface.blit(font.render(message, 1, color), pos)

# Events
evTime = pygame.USEREVENT+4
evTurn = pygame.USEREVENT+3
evCreateLife = pygame.USEREVENT+1
evGrowFood = pygame.USEREVENT+2

# Timers
pygame.time.set_timer(evCreateLife, int(5000/speed))
pygame.time.set_timer(evTime, int(1000/speed))
pygame.time.set_timer(evGrowFood, int(3000/speed))
pygame.time.set_timer(evTurn, int(10/speed))


# Lists
LifeForms = []
FoodForms = []

#newLife = Life()
#x, y = random.randint(0, width), random.randint(0, height)
#newLife.Birth(surface, "Bobby", x, y, "red")
#LifeForms.append(newLife)
#print("Created: ", "Bobby" + str(a), x, y)

Day = 0
Hour = 0

while True:
    clock.tick(100)
    surface.fill((0,0,0))
    for lifeForm in LifeForms:
        pygame.draw.circle(surface, colors[lifeForm.color], (lifeForm.x, lifeForm.y), lifeForm.radius)
        drawText(surface, str(lifeForm.Food), (lifeForm.x, lifeForm.y))
        lifeForm.detectColissions()
    for foodForm in FoodForms:
        pygame.draw.circle(surface, colors[foodForm.color], (foodForm.x, foodForm.y), foodForm.radius)
    for e in pygame.event.get():
        if e.type == evTime:
            Hour += 1
            if Hour == 24:
                for lifeForm in LifeForms:
                    lifeForm.Food -= 1
                    if lifeForm.Food == -2:
                        lifeForm.Kill()
                    elif lifeForm.Food < 0:
                        lifeForm.color="dred"
                    else:
                        lifeForm.color = "red"
                Hour = 0
                Day+=1
        if e.type == evTurn:
            for lifeForm in LifeForms:
                if len(FoodForms) > 0:
                    x,y = lifeForm.locateClosestFood()
                    lifeForm.Move(x,y)
        if e.type == evCreateLife:
            CreateLife()
        if e.type == evGrowFood:
            GrowFood()
    drawText(surface, str("Day: " + str(Day) + ", Hour: " + str(Hour) + " | Life forms: " + str(len(LifeForms))), (0,0))
    pygame.display.flip()
