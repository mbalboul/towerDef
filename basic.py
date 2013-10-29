import sys, pygame, random
from pygame.locals import *

pygame.init()
pygame.font.init()
random.seed()

enemyManager = 0
arrowManager = 0
totalTime = 0
scoreFont = pygame.font.Font(None, 24)

#Set of classes for the game
class Enemy(pygame.sprite.Sprite): #I SHOULD make enemy an overall superclass and move this to a NormalEnemy
    #def __init__(self):
    #    self.__g = {} # The groups the sprite is in
        #if groups: self.add(groups)
    #    self.pic = pygame.image.load("enemy_norm.png")
    #    self.rect = pygame.Rect(-32, 224, 32, 32) #convenient starting position
    
    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)
        self.pic = pygame.image.load("enemy_norm.png")
        self.rect = pygame.Rect(-32, 224, 32, 32)
        self.health = 2
        
    def move(self): 
        self.rect = self.rect.move(1,0)
        screen.blit(self.pic, self.rect)
        
    def hurt(self):
        self.health -= 1
        self.pic = pygame.image.load("enemy_hit.png")
        if (self.health==0): enemyManager.scoreInc(); self.kill()

class FastEnemy(pygame.sprite.Sprite): 
    def __init__(self, *args, **kwargs):
        super(FastEnemy, self).__init__(*args, **kwargs)
        self.pic = pygame.image.load("enemy_norm_scary.png")
        self.rect = pygame.Rect(-32, 224, 32, 32)
        self.health = 1
        
    def move(self): 
        self.rect = self.rect.move(5,0)
        screen.blit(self.pic, self.rect)
        
    def hurt(self): enemyManager.scoreInc(); self.kill()
    
class TankEnemy(pygame.sprite.Sprite): 
    def __init__(self, *args, **kwargs):
        super(TankEnemy, self).__init__(*args, **kwargs)
        self.pic = pygame.image.load("enemy_norm_scary.png")
        self.rect = pygame.Rect(-32, 224, 32, 32)
        self.health = 5
        
    def move(self): 
        self.rect = self.rect.move(1,0)
        screen.blit(self.pic, self.rect)
        
    def hurt(self):
        self.health -= 1
        self.pic = pygame.image.load("enemy_hit_scary.png")
        if (self.health==0): enemyManager.scoreInc(); self.kill()

class Arrow(pygame.sprite.Sprite):
    #def __init__(self):
    #    self.__g = {} # The groups the sprite is in
        #if groups: self.add(groups)
    #    self.pic = pygame.image.load("arrow.png")
    #    self.rect = pygame.Rect(576, 232, 32, 16)
    
    def __init__(self, *args, **kwargs):
        super(Arrow, self).__init__(*args, **kwargs)
        self.pic = pygame.image.load("arrow.png")
        self.rect = pygame.Rect(576, 232, 32, 16)
    
    def move(self): 
        self.rect = self.rect.move(-8,0)
        screen.blit(self.pic, self.rect)
        
    #set a method that damages the opponent arrow with Rect.colliderect()

class EnemyManager(pygame.sprite.RenderClear):
    def timerInit(self):
        self.timer = 0;
        self.score = 0;
        
    def scoreInc(self):
        self.score+=1;
    
    def manage(self): #Moves all enemies, adds a new one if enough time has passed
        self.sprites()
        for i in self.sprites(): #Moves all enemies
            i.move() 
            if (i.rect.right>577): #THIS IS THE KILL METHOD.  THIS ENDS THE GAME.
                print (format(totalTime) + " time units")
                print (format(self.score) + " kills")
                print (format(self.score*1000/totalTime) + " killocity")
                if (totalTime<500): print("Try again...")
                elif (totalTime<1000): print("Terrible...")
                elif (totalTime<1500): print("At least you tried.")
                elif (totalTime<2000): print("Not bad.")
                elif (totalTime<2500): print("Pretty good!")
                elif (totalTime<3000): print("Great work!")
                elif (totalTime<3500): print("Verrry impressive!")
                else: print("You're serious business, huh?")
                if (self.score>250): print("And you got a great kill count too!")
                sys.exit()
        self.timer += 1
        
        #if (len(self.enemies)>0 and len(self.arrows)>0): #The third part.
        #    if (self.enemies[0].rect.colliderect(self.arrows[0].rect)):
        #        self.enemies.popleft()
        #This old code performed a function that groupcollide() takes care of.
        
        if (self.timer*random.randint(90,(90+totalTime/1))>10000): #Adds a new enemy if time constraints are met.
            #self.add(Enemy())
            randomizer = random.randint(1,8) #What type of enemy to add?
            if (randomizer < 6): self.add(Enemy()) #change this to randomize it.
            elif (randomizer < 8): self.add(FastEnemy())
            else: self.add(TankEnemy())
            self.timer = 0
        
class ArrowManager(pygame.sprite.RenderClear):
        
    def manage(self): #Moves all arrows, degrades arrows offscreen, and adds new ones per click
        for i in self.sprites(): 
            i.move() #Moves all arrows
            if (i.rect.right<0): self.remove(i) #degrades offscreen arrows
        
    def shootArrow(self): self.add(Arrow())

#This is all the prepwork.  
tower = pygame.image.load("tower.png")
bg = pygame.image.load("background-cyan.png")
enemyManager = EnemyManager()
arrowManager = ArrowManager()
enemyManager.timerInit()
screen = pygame.display.set_mode([640, 480])
#screen.blit(bg,[0,0])
screen.fill([143,239,239])
screen.blit(tower, [576, 208])
pygame.display.flip()
    
while(1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit() #a quit event
        
        if event.type == MOUSEBUTTONDOWN: arrowManager.shootArrow()
        
    pygame.time.wait(10) #We don't want the enemy to run too fast.
    #screen.blit(bg,[0,0])
    screen.fill([143,239,239])
    screen.blit(tower, [576, 208])
    screen.blit(scoreFont.render(format(totalTime), 0, [240,64,64]), [0,0])
    screen.blit(scoreFont.render(format(enemyManager.score) + " enemies killed", 0, [240,64,64]), [0,24])
    screen.blit(scoreFont.render(format(enemyManager.score*1000/(totalTime+1)) + " killocity", 0, [240,64,64]), [0,48])
    totalTime += 1
    enemyManager.manage()
    arrowManager.manage()
    pygame.display.update()
    
    #This next set of stuff handles collisions
    collisionset = pygame.sprite.groupcollide(enemyManager, arrowManager, 0, 1)
    if (collisionset):
        for i in collisionset:
            i.hurt()
    
    
    
#CREATE A CLASS THAT MANAGES ENEMIES BY MAINTAINING A LIST OF ALL ENEMIES
#THE CLASS WILL HAVE A MOVE FUNCTION THAT MOVES ALL ENEMIES BY REFERENCING ALL OF THEM.