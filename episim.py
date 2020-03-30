import pygame
from random import randrange, randint
from time import sleep
from math import sqrt

# pygame world size
worldXY = (180,130)         # x, y
size = 5                    # one person - pygame rectangle
peoples = 1000

# main simulation variables
threshold_resistance = 10   # 0 - nobody / test 30
                            # = a totally resistant percentage of the population
                            
dist_infect = 3             # distance - infection 3 (100*100)/ 5 / 7 / 10

bmax = 3                    # brownian motion  1,2,3, 5
                            # 2 => random (-2,-1,0,1,2)

serious_critical = 10       # (magenta) 5-20%

time_infect = 7             # (yelow) 5/7/9 days (or "double" days)/ all active_cases
                            # = incubation period without symptoms
time_cure = 30              # testing - the time required for complete cure                    
                            

colYel = (255,255,0)
colWhi = (255,255,255)
colRed = (255,0,0)
colOra = (255,126,0)
colMag = (255,0,255)
colBlu = (0,0,255)
colSil = (200,200,200)
colBla = (0,0,0) 

sizeWinX = worldXY[0] * size + 150
sizeWinY = worldXY[1] * size + 35

print("init_screen")
pygame.init()
font = pygame.font.SysFont("comicsansms", 18)

screen = pygame.display.set_mode([sizeWinX,sizeWinY]) # Create the pygame window
screen.fill(colSil)
text = font.render("Infection | Simulation", True, colRed)
screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
pygame.display.flip()
sleep(2)

screen.fill(colSil)
pygame.display.flip()


# text position:
xi = sizeWinX - 90
yiadd = 25
yi1 = 60

# chart position:
chy = 600
chx = xi-30
ydel = 2


print("start-simulator")


def distance(x1,y1,x2,y2):
    x = abs(x1-x2)
    y = abs(y1-y2)
    return sqrt(x*x + y*y)


class People():
    def __init__(self, i, z = 0):
        self.i = i
        self.resistance = randrange(100)
        if (i == 5): # prvni nakazeny
             self.x = worldXY[0]/2
             self.y = worldXY[1]/2
        else:    
             self.x = randrange(worldXY[0])
             self.y = randrange(worldXY[1])
        # self.z = randrange(0,10)
        self.z = i
        self.time = 0
        self.ti = 0 # time infection

    def day(self):
        self.time += 1
        
    def info(self):
        print(self.i,self.x,self.y,self.z)

    def ds_show(self, col): #direct single
        pygame.draw.rect(screen,col,(self.x*size,self.y*size,size,size))
        pygame.display.flip()



class World():
    def __init__(self, n=10):
        self.num = n
        self.old_inf = 1
        self.w = []
        for i in range(self.num):
            self.w.append(People(i))

    def info(self): 
        i = 0
        for i in range(self.num):
            print(self.w[i].info())
            i += 1

    def brown(self, show = True):        
        for i in range(self.num):
            if show:
               self.w[i].ds_show(colSil)
               pygame.display.flip()
        
            self.w[i].x += randint(-bmax,bmax)
            if (self.w[i].x < 0): self.w[i].x = 0
            if (self.w[i].x > worldXY[0]): self.w[i].x = worldXY[0]
            self.w[i].y += randint(-bmax,bmax)
            if (self.w[i].y < 0): self.w[i].y = 0
            if (self.w[i].y > worldXY[1]): self.w[i].y = worldXY[1]

            if show:
                if self.w[i].ti > time_cure: # test
                    self.w[i].z = 6
                    self.w[i].resistance = 90
                
                if self.w[i].z == 5:
                    col = colRed
                    if self.w[i].ti > time_infect:
                        if self.w[i].resistance > serious_critical:
                            col = colYel
                        else:
                            col = colMag # serious critical

                else:
                    col = colBla
                    
                if self.w[i].resistance > 100-threshold_resistance:
                    col = colBlu
                    
                self.w[i].ds_show(col)
                pygame.display.flip()

    def infection(self, world_time):
        numi = 0
        numti = 0
        numtic = 0
        
        for i in range(self.num):
            if self.w[i].z == 5:
               self.w[i].ti += 1 
               numi += 1         
        
               # test
               for j in range(self.num):
                   if self.w[j].resistance <= 100-threshold_resistance:
                      dist = distance(self.w[i].x, self.w[i].y, self.w[j].x, self.w[j].y) 
                      if dist < dist_infect:
                           self.w[j].z = 5
               if self.w[i].ti > time_infect:
                   numti += 1
                   if self.w[i].resistance <= serious_critical:
                       numtic +=1
                    

        r0 = numi / self.old_inf
        self.old_inf = numi
        
        # text:
        text1 = font.render(str(world_time) + " | "+ str(r0), True, colBlu)
        text2 = font.render(str(numi), True, colRed)
        text3 = font.render(str(numti), True, colYel)
        text4 = font.render(str(numtic), True, colMag)
        pygame.draw.rect(screen,colSil,(xi,yi1,130,150))
        screen.blit(text1, (xi, yi1))
        screen.blit(text2, (xi, yi1 + yiadd))
        screen.blit(text3, (xi, yi1 + yiadd * 2))
        screen.blit(text4, (xi, yi1 + yiadd * 3))
        
        # chart:
        pygame.draw.rect(screen,colRed,(chx+world_time*2,chy-numi/ydel,2,numi/ydel))
        pygame.draw.rect(screen,colYel,(chx+world_time*2,chy-numti/ydel,2,numti/ydel))
        pygame.draw.rect(screen,colMag,(chx+world_time*2,chy-numtic/ydel,2,numtic/ydel))
        pygame.draw.rect(screen,colBlu,(chx+world_time*2,chy-int(r0/ydel*100),2,2))
        pygame.draw.line(screen,colBla,(chx,chy),(xi+100,chy))
        pygame.draw.line(screen,colBla,(chx,chy-100/ydel),(chx+100,chy-100/ydel))
        pygame.draw.line(screen,colBla,(chx,chy-200/ydel),(chx+100,chy-200/ydel))
        pygame.display.flip()


    def show(self):
        i = 0
        for i in range(self.num):
            if self.w[i].z == 5:
                col = colRed
            else:
                col = colBla
            self.w[i].ds_show(col)
            print()
            i += 1
        pygame.display.flip()

    def clear(self):
        screen.fill(colSil)
        pygame.display.flip()


class Simulation:
    def step(self, world_time):
        w.infection(world_time)
        w.brown()

    def run(self, count=51):
        for world_time in range(count): # number of steps (days)
            self.step(world_time)


# =============== main =====================
w = World(peoples)

text_info = "epidemic simulation: peoples " + str(peoples) + " | resistence " +  str(threshold_resistance) + "% | inf.distance " + str(dist_infect) + " | move " + str(bmax)
text = font.render(text_info, True, colBla)
screen.blit(text, (10, sizeWinY-30))
pygame.display.flip()

simulation = Simulation()
simulation.run()
