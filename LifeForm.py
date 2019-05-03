#from Evolution1.main import getLifeForms, getFoodForms, RemoveFood, RemoveLife

class Life:

    name = "Generic Life Form"
    x = 0
    y = 0
    color = "Blue"
    radius = 15

    Food = 0

    ini_speed = 1
    speed = 1

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
    def locateClosestLife(self):
        LifeForms = self.getLifeForms()
        closest = LifeForms[0]
        closestVal = self.distanceTo(closest.x,closest.y)
        for lifeForm in LifeForms:
            if self.distanceTo(lifeForm.x,lifeForm.y) < closestVal:
                closest = lifeForm
                closestVal=self.distanceTo(lifeForm.x,lifeForm.y)
        return closest.x, closest.y