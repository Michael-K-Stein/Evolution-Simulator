import math
import random
from random import shuffle
import pygame
from pygame import Color
from Evolution1.Generics import colors
from Evolution1.Graphics import WorldSim
from Evolution1.LifeForm import Life
#from Evolution1.FoodForm import Food

lPopulation = []
lAverageSpeed = []

def listPrint(l):
    for p in l:
        #print(p)
        break

def EndSimulation():
    #print(Population)
    #print(AverageSpeed)
    #listPrint(Population)
    lPopulation.append(Population)
    lAverageSpeed.append(AverageSpeed)
    exit()

class Food:

    name = "Generic Food Form"
    x = 0
    y = 0
    color = Color(255,255,0,0)
    radius = 5

    feed = 1

    def Grow(self, surface, x, y, feed):
        self.x = x
        self.y = y
        self.surface = surface
        self.feed = feed
        self.radius = 4 + feed

    def Remove(self):
        self.color = colors["brown"]
        RemoveFood(self)

class Life:

    name = "Generic Life Form"
    x = 0
    y = 0
    color = Color(255,0,0,0)
    radius = 15
    sexy = 1

    Food = 1

    ini_speed = 1
    speed = 1

    intelligence = 2
    Violence = 0
    Altruism = 0

    offsprings = 0

    life = 144

    def Think(self):
        if self.Violence == 0:
            if self.Food < 6:
                if len(self.getFoodForms()) > 0:
                    if self.intelligence >= 3:
                        x, y = self.locateSmartClosestFood()
                    else:
                        x, y = self.locateClosestFood()
                    self.Move(x, y)
            else:
                if self.closestLife().Food > 6 or self.intelligence < 2:
                    # Look for sex
                    x, y = self.locateClosestLife()
                    self.Move(x, y)
                else:
                    if len(self.getFoodForms()) > 0:
                        if self.intelligence >= 3:
                            x,y = self.locateSmartClosestFood()
                        else:
                            x, y = self.locateClosestFood()
                        self.Move(x, y)
        elif self.Violence >= 1:
            if self.Food < 6:
                if len(self.getFoodForms()) > 0:
                    if self.intelligence >= 3:
                        x, y = self.locateSmartClosestFood()
                    else:
                        x, y = self.locateClosestFood()
                    clLife = self.closestLife()
                    x1, y1 = clLife.x, clLife.y
                    d = self.distanceTo(x1,y1)
                    if d < self.distanceTo(x,y):
                        if d < self.radius + clLife.radius:
                            self.Murder(clLife)
                        else:
                            self.Move(x1, y1)
                    else:
                        self.Move(x,y)
            else:
                if self.closestLife().Food > 6 or self.intelligence < 2:
                    # Look for sex
                    x, y = self.locateClosestLife()
                    self.Move(x, y)
                else:
                    if len(self.getFoodForms()) > 0:
                        if self.intelligence >= 3:
                            x,y = self.locateSmartClosestFood()
                        else:
                            x, y = self.locateClosestFood()
                        self.Move(x, y)


    def Birth(self, surface, name, x, y, color, ini_speed, sexy, intelligence, Altruism=0, Violence=0):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.surface = surface
        self.sexy = sexy
        self.ini_speed = ini_speed
        self.intelligence = intelligence
        self.Violence = Violence
        self.Altruism = Altruism

    def Kill(self):
        #self.x=0
        #self.y=0
        #self.color = "Brown"
        #self.name = "Deceased (" + self.name +")"
        RemoveLife(self)
        self.life = 144
        self.offsprings = 0

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
        for lifeForm in self.getLifeFormsNotMe():
            if self.distanceTo(lifeForm.x, lifeForm.y) < lifeForm.radius + self.radius:
                self.TryToReproduce(lifeForm)

    lastLifeFormColission = None
    colissionTimes = 0
    def PunishForClotting(self):
        colided = None
        for lifeForm in self.getLifeFormsNotMe():
            if self.distanceTo(lifeForm.x, lifeForm.y) < lifeForm.radius + self.radius:
                colided = lifeForm
                if self.lastLifeFormColission == lifeForm:
                    self.Food -= self.colissionTimes
                    self.colissionTimes += 1
                    self.x += pm(self.radius)
                    self.y += pm(self.radius)
                else:
                    self.lastLifeFormColission = lifeForm
                    self.colissionTimes = 0
        if colided == None:
            self.lastLifeFormColission = None
            self.colissionTimes = 0

    def Murder(self, lifeForm):
        self.Food += lifeForm.Food
        self.ini_speed =(lifeForm.speed / 10) + self.ini_speed
        self.intelligence = (lifeForm.intelligence / 10) + self.intelligence
        self.sexy -= 0.1 * self.sexy
        lifeForm.Kill()
        print(self.name,"Murdering: " + lifeForm.name)

    def TryToReproduce(self, partner):
        #print("Trying to fuck", "Will it work? ", randomChance(5 / ((self.sexy + partner.sexy)/2)) and self.Food > 5 and partner.Food > 5)
        if self.Food > 5 and partner.Food > 5:
            if randomChance(5 / ((self.sexy + partner.sexy)/2)):
                newLife = Life()
                x, y = int((self.x + partner.x)/2),int((self.y + partner.y)/2)
                n = randomName(True)
                newLife.Birth(surface, n, x, y, self.averageColor(partner),mut((self.ini_speed+partner.ini_speed)/2),mut((self.sexy+partner.sexy)/2),mut((self.intelligence+partner.intelligence)/2))
                LifeForms.append(newLife)
                #print(n,"was born!")
                self.Food-=5
                partner.Food-=5
                self.offsprings+=1
            elif self.Violence>=2:
                self.Food-=5
                partner.Food-=5
                clLife = self.closestLife()
                x1, y1 = clLife.x, clLife.y
                d = self.distanceTo(x1, y1)
                if d < self.radius + clLife.radius:
                    self.Murder(clLife)
                else:
                    self.Move(x1, y1)

    def averageColor(self,partner):
        r,g,b=int(mut((self.color.r + partner.color.r)/2)),int(mut((self.color.g + partner.color.g)/2)),int(mut((self.color.b + partner.color.b)/2))
        if r>255: r=255
        if g>255: g=255
        if b>255: b=255
        return pygame.Color( r,g,b,0 )

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

    def locateSmartClosestFood(self):
        FoodForms = self.getFoodForms()
        closest = FoodForms[0]
        closestVal = self.distanceTo(closest.x,closest.y)
        for foodForm in FoodForms:
            if  (self.distanceTo(foodForm.x,foodForm.y)/Food.feed < closestVal):
                closest = foodForm
                closestVal=self.distanceTo(foodForm.x,foodForm.y)/Food.feed
        return closest.x, closest.y

    def eat(self, food):
        self.Food += food
        self.radius = 15 + int(abs(self.Food)**0.5)
        if self.Food > 10:
            self.speed = math.ceil(self.ini_speed * ((self.Food / 10)**0.5))
        else:
            self.speed = math.ceil(self.ini_speed)

    def locateClosestLife(self):
        aLifeForms = self.getLifeFormsNotMe()
        if not len(aLifeForms) == 0:
            closest = aLifeForms[0]
            closestVal = self.distanceTo(closest.x,closest.y)
            for lifeForm in aLifeForms:
                if self.distanceTo(lifeForm.x,lifeForm.y) < closestVal and lifeForm.Food>5:
                    closest = lifeForm
                    closestVal=self.distanceTo(lifeForm.x,lifeForm.y)
            return closest.x+closest.radius, closest.y+closest.radius
        else:
            EndSimulation()
            return self

    def closestLife(self):
        aLifeForms = self.getLifeFormsNotMe()
        if not len(aLifeForms) == 0:
            closest = aLifeForms[0]
            closestVal = self.distanceTo(closest.x,closest.y)
            for lifeForm in aLifeForms:
                if self.distanceTo(lifeForm.x,lifeForm.y) < closestVal and lifeForm.Food>5:
                    closest = lifeForm
                    closestVal=self.distanceTo(lifeForm.x,lifeForm.y)
            return closest
        else:
            EndSimulation()
            return self

    def getLifeForms(self):
        return LifeForms
    def getFoodForms(self):
        return FoodForms
    def getLifeFormsNotMe(self):
        tmpLifeForms = LifeForms.copy()
        try:
            tmpLifeForms.remove(self)
        except:
            return tmpLifeForms
        return tmpLifeForms

def randomChance(d): # Boolean with a chance of 1/d of giving True
    rndNum = random.random()
    if rndNum <= 1/d:
        return True
    else:
        return False

def pm(val):
    if randomChance(2):
        return val
    else:
        return -val

def RemoveFood(foodForm):
    FoodForms.remove(foodForm)
def RemoveLife(lifeForm):
    LifeForms.remove(lifeForm)

def randomName(bboy):
    r = random.randint(0,4945)
    n = ""
    fp = open("RandomNames")
    for i, line in enumerate(fp):
        if i == r:
            n = line[0:len(line)-1]
            break
    fp.close()
    return n

def appendLine(ind, val):
    with open('PopulationResults', 'r') as file:
        data = file.readlines()
    ln = data[ind]
    #print(ln,"","","",str(val) + "\t" + ln)
    data[ind] = str(val) + "\t" + ln
    with open('PopulationResults', 'w') as file:
        file.writelines(data)

def mut(val):
    if randomChance(mutationRate):
        return val * (1+mutationFactor)
    else:
        return val * (1-mutationFactor)

#print("Starting World")

# Definitions

speed = 2
width = 1200
height = 800

mutationFactor = 0.1 # Change caused by mutation
mutationRate = 2 # 1 in this many
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
        #print("Created: ", "Gen" + str(a), x, y)
def GrowFood():
    if randomChance(2):
        newFood = Food()
        x, y = random.randint(0, width), random.randint(0, height)
        newFood.Grow(surface, x, y, 1)
        FoodForms.append(newFood)
    if randomChance(3):
        newFood = Food()
        x, y = random.randint(0, width), random.randint(0, height)
        newFood.Grow(surface, x, y, 2)
        FoodForms.append(newFood)
    if randomChance(5):
        newFood = Food()
        x, y = random.randint(0, width), random.randint(0, height)
        newFood.Grow(surface, x, y, 4)
        FoodForms.append(newFood)
    if randomChance(10):
        newFood = Food()
        x, y = random.randint(0, width), random.randint(0, height)
        newFood.Grow(surface, x, y, 8)
        FoodForms.append(newFood)
    if randomChance(200):
        newFood = Food()
        x, y = random.randint(0, width), random.randint(0, height)
        newFood.Grow(surface, x, y, 100)
        FoodForms.append(newFood)

font = pygame.font.SysFont('Ubuntu',20,True)
def drawText(surface, message, pos, color=(255, 255, 255)):
    surface.blit(font.render(message, 1, color), pos)

# Events
evTime = pygame.USEREVENT+4
evTurn = pygame.USEREVENT+3
#evCreateLife = pygame.USEREVENT+1
evGrowFood = pygame.USEREVENT+2

# Timers
#pygame.time.set_timer(evCreateLife, int(5000/speed))
pygame.time.set_timer(evTime, int(1000/speed))
pygame.time.set_timer(evGrowFood, int(100/speed))
pygame.time.set_timer(evTurn, int(10/speed))


# Lists
LifeForms = []
FoodForms = []

Adam = Life()
x, y = random.randint(0, width), random.randint(0, height)
#Adam.Birth(surface, "Adam", x, y, Color(0,191,255,0), 2 * speed, 1, 1)
Adam.Birth(surface, "Adam", x, y, Color(255,0,0,0), 1 * speed, 1, 1, Violence=2)
LifeForms.append(Adam)

Eve = Life()
x, y = random.randint(0, width), random.randint(0, height)
#Eve.Birth(surface, "Eve", x, y, Color(255,20,147,0), 1 * speed, 1, 2)
Eve.Birth(surface, "Eve", x, y, Color(0,255,0,0), 1 * speed, 2, 2)
LifeForms.append(Eve)

Adam2 = Life()
x, y = random.randint(0, width), random.randint(0, height)
Adam2.Birth(surface, "Adam2", x, y, Color(0,0,255,0), 1 * speed, 1, 4)
LifeForms.append(Adam2)

Eve2 = Life()
x, y = random.randint(0, width), random.randint(0, height)
Eve2.Birth(surface, "Eve2", x, y, Color(255,255,0,0), 1 * speed, 100, 2)
LifeForms.append(Eve2)

def getBestLifeForm():
    best = LifeForms[0]
    best_val = best.offsprings
    for lifeForm in LifeForms:
        if lifeForm.offsprings > best_val:
            best = lifeForm
            best_val = best.offsprings
        elif lifeForm.offsprings==best_val and lifeForm.Food>best.Food:
            best = lifeForm
            best_val = best.offsprings
    return best

def getAverageLifeFormSpeed():
    sum = 0
    for lifeForm in LifeForms:
        sum += lifeForm.speed
    return sum/len(LifeForms)

# Data:
Population = []
AverageSpeed = []
Simulate = True
Day = 0
Hour = 0

while Simulate:
    clock.tick(100)
    surface.fill((0,0,0))
    for lifeForm in LifeForms:
        pygame.draw.circle(surface, lifeForm.color, (lifeForm.x, lifeForm.y), lifeForm.radius)
        drawText(surface, str(int(lifeForm.Food)), (lifeForm.x, lifeForm.y),color=(0,0,0))
        #drawText(surface, str(lifeForm.speed), (lifeForm.x, lifeForm.y-10))
        lifeForm.detectColissions()
    for foodForm in FoodForms:
        pygame.draw.circle(surface, foodForm.color, (foodForm.x, foodForm.y), foodForm.radius)
    for e in pygame.event.get():
        if e.type == evTime:
            Hour += 1
            #print(len(LifeForms))
            appendLine(Day*24 +  Hour-1,len(LifeForms))
            #Population.append(len(LifeForms))
            #AverageSpeed.append(getAverageLifeFormSpeed())
            shuffle(LifeForms)
            for lifeForm in LifeForms:
                lifeForm.life-=1
                if lifeForm.life == 0 or lifeForm.Food<0:
                    lifeForm.Kill()
                lifeForm.PunishForClotting()
                lifeForm.Food -= 0.1
            if Hour == 24:
                for lifeForm in LifeForms:
                    lifeForm.Food -= 1
                    if lifeForm.Food == -2:
                        lifeForm.Kill()
                Hour = 0
                Day+=1
            if Day == 200:
                Adam.Food = 0
                Eve.Food = 0
                LifeForms = [Adam, Eve]
                FoodForms = []
                Hour = 0
                Day = 0
            if Day == 200:
                Simulate = False
        if e.type == evTurn:
            for lifeForm in LifeForms:
                lifeForm.Think()
        #if e.type == evCreateLife:
        #    CreateLife()
        if e.type == evGrowFood:
            GrowFood()
    if pygame.key.get_pressed()[pygame.K_KP9] != 0:
        EndSimulation()
    drawText(surface, str("Day: " + str(Day) + ", Hour: " + str(Hour) + " | Life forms: " + str(len(LifeForms))), (0,0))
    bestLifeForm = getBestLifeForm()
    drawText(surface, str("Best: " + bestLifeForm.name + " | Offsprings: "+str(bestLifeForm.offsprings) + " | Speed: " + str(bestLifeForm.speed)), (0,20))
    pygame.display.flip()
EndSimulation()