#!/usr/bin/env python3
# The MIT License (MIT)
# 1 or 2 worls

import pygame
from random import randrange, randint
from time import sleep
from math import sqrt

# pygame world size
worldXY = (180,130)         # x, y
size = 3                    # one person - pygame rectangle
people = 1500

# main simulation variables
threshold_resistance = 15   # 0 - nobody / test 30
                            # = a totally resistant percentage of the population
                            
dist_infect = 2             # distance - infection 3 (100*100)/ 5 / 7 / 10

brown_mov_max = 3           # (int) brownian motion  1,2,3, 5
                            # 2 => random (-2,-1,0,1,2)

serious_critical = 10       # (magenta) 5-20%

time_infect = 7             # (yelow) 5/7/9 days (or "double" days)/ all active_cases
                            # = incubation period without symptoms
time_cure = 30              # 30 - testing - the time required for complete cure                    

slow_show = False           # True: every Person step by step move
                            # False: all wordl step
steps_of_simulation = 180

#----------------------------------------------------
# slow_show = input("Fast or slow? 1/0: ")

#----------------------------------------------------
colBla = (0,0,0)        # not infected
colBlu = (0,0,255)      # resistant
colRed = (255,0,0)      # infected - asymptomatic
colYel = (255,255,0)    # symptomatic infected
colMag = (255,0,255)    # critical condition
colGre = (0,255,0)      # recovered 
colSil = (200,200,200)  # recovered and resistant
colOra = (255,126,0)
colWhi = (255,255,255)

numWorlds = 2 #

sizeWinX = worldXY[0] * size * numWorlds + 30
sizeWinY = worldXY[1] * size  + 250

print("init_screen")
pygame.init()
pygame.display.set_caption('Epidemic simulator 2.0')
font = pygame.font.SysFont("verdana", 12)

# text position:
xi = 20
yiadd = 20
yi1 = sizeWinY - 230

# chart position:
chy = 600
chx = 150
ydel = people/500


class Person():
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
        self.ti = 0 # time infection

    def info(self):
        print(self.i,self.x,self.y,self.z)

    def distance(self, other):
         x = abs(self.x - other.x)
         y = abs(self.y - other.y)
         return sqrt(x*x + y*y)

    def ds_show(self, screen, col, flip = True, ofx = 0): #direct single
        pygame.draw.rect(screen,col,(self.x*size + ofx,self.y*size,size,size))
        if flip:
            pygame.display.flip()


class World():
    def __init__(self, n=10, ofx=0, ofy=0):
        self.num = n
        self.old_inf = 1
        self.ofx = ofx
        self.ofy = ofy
        self.people = []
        for i in range(self.num):
            self.people.append(Person(i))

    def info(self):
        i = 0
        for i in range(self.num):
            print(self.people[i].info())
            i += 1

    def brown(self, screen, slow_show = slow_show):
        for i in range(self.num):
            self.people[i].ds_show(screen, colSil, slow_show, ofx = self.ofx) # xxx ofx = self.ofx > art
        
            self.people[i].x += randint(-brown_mov_max,brown_mov_max)
            if (self.people[i].x < 0): self.people[i].x = 0
            if (self.people[i].x > worldXY[0]): self.people[i].x = worldXY[0]
            self.people[i].y += randint(-brown_mov_max,brown_mov_max)
            if (self.people[i].y < 0): self.people[i].y = 0
            if (self.people[i].y > worldXY[1]): self.people[i].y = worldXY[1]

            if self.people[i].ti > time_cure: # test
                self.people[i].z = 6
                self.people[i].resistance = 90

            if self.people[i].resistance > 100-threshold_resistance:
                col = colBlu
            else:
                col = colBla
            
            if self.people[i].z == 5:
                col = colRed
                if self.people[i].ti > time_infect:
                    if self.people[i].resistance > serious_critical:
                        if self.people[i].resistance < 50:
                            col = colYel
                        else:
                            col = colOra
                    else:
                        col = colMag # serious critical

            elif self.people[i].z == 6:
                col = colGre
                
            self.people[i].ds_show(screen, col,slow_show, ofx = self.ofx)

    def infection(self, screen, world_time):
        numi = 0
        numti = 0
        numtic = 0
        numtir = 0
        
        for i in range(self.num):
            if self.people[i].z == 6:
               numtir += 1
               
            if self.people[i].z == 5:
               self.people[i].ti += 1 
               numi += 1         
        
               # test
               for j in range(self.num):
                   if self.people[j].resistance <= 100-threshold_resistance:
                      dist = self.people[i].distance(self.people[j])
                      if dist < dist_infect:
                           self.people[j].z = 5
               if self.people[i].ti > time_infect:
                   numti += 1
                   if self.people[i].resistance <= serious_critical:
                       numtic +=1
                    
        if (self.old_inf > 0):
            r0 = round(numi / self.old_inf, 3)
        else:
            r0 = 0

        self.old_inf = numi

        # text:
        text1 = font.render("time: " + str(world_time) + " | R0: "+ str(r0), True, colBla)
        text2 = font.render("infected " + str(numi), True, colRed)
        text3 = font.render("symptom. " + str(numti), True, colYel)
        text4 = font.render("critical " + str(numtic), True, colMag)
        text5 = font.render("rerover. " + str(numtir), True, colGre)
        pygame.draw.rect(screen,colSil,(self.ofx+xi,yi1,130,170))
        screen.blit(text1, (self.ofx+xi, yi1))
        screen.blit(text2, (self.ofx+xi, yi1 + yiadd))
        screen.blit(text3, (self.ofx+xi, yi1 + yiadd * 2))
        screen.blit(text4, (self.ofx+xi, yi1 + yiadd * 3))
        screen.blit(text5, (self.ofx+xi, yi1 + yiadd * 4))
        
        # chart:
        td = 2000/self.num  # steps > 70: 1 / 2
        pygame.draw.line(screen,colBla,(worldXY[0] * size + 10, 0),(worldXY[0] * size + 10, sizeWinY))
        pygame.draw.rect(screen,colRed,(self.ofx+chx+world_time*td,chy-numi/ydel,2,numi/ydel))
        pygame.draw.rect(screen,colYel,(self.ofx+chx+world_time*td,chy-numti/ydel,2,numti/ydel))
        pygame.draw.rect(screen,colMag,(self.ofx+chx+world_time*td,chy-numtic/ydel,2,numtic/ydel))
        pygame.draw.rect(screen,colBlu,(self.ofx+chx+world_time*td,chy-int(r0/ydel*100),2,2))
        pygame.draw.rect(screen,colGre,(self.ofx+chx+world_time*td,chy-numtir/ydel,2,2))
        pygame.draw.line(screen,colBla,(self.ofx+chx,chy),(self.ofx+xi+steps_of_simulation*td,chy))
        pygame.draw.line(screen,colBla,(self.ofx+chx,chy-100/ydel),(self.ofx+chx+steps_of_simulation*td,chy-100/ydel))
        pygame.draw.line(screen,colBla,(self.ofx+chx,chy-200/ydel),(self.ofx+chx+steps_of_simulation*td,chy-200/ydel))


    def show(self):
        i = 0
        for i in range(self.num):
            if self.people[i].z == 5:
                col = colRed
            else:
                col = colBla
            self.people[i].ds_show(col, ofx = self.ofx)
            print()
            i += 1
        #pygame.display.flip()


class Simulation:
    def __init__(self, text_info, count):
        self.text_info = text_info
        self.count = count
        self.worlds = []

    def add(self, world):
        self.worlds.append(world)

    def init(self):
        screen = self.screen = pygame.display.set_mode([sizeWinX,sizeWinY]) # Create the pygame window
        screen.fill(colSil)
        text = font.render("Epidemic | Simulation", True, colRed)
        screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.display.flip()
        sleep(2)

        screen.fill(colSil)        
        pygame.display.flip()

        text = font.render(self.text_info, True, colBla)
        screen.blit(text, (10, sizeWinY-30))
        pygame.display.flip()

    def step(self, world_time):
        for world in self.worlds:
            world.infection(self.screen, world_time)
            world.brown(self.screen)
            pygame.display.flip()

    def run(self):
        self.init()
        for world_time in range(self.count + 1): # number of steps (days)
            # if ....
            self.step(world_time)


# =============== main =================
text_info = "people " + str(people) + " | resistence " +  str(threshold_resistance) + "% | inf.distance " + str(dist_infect) + " | move " + str(brown_mov_max)
init_vector = (people, threshold_resistance, dist_infect, brown_mov_max)
simulation = Simulation(text_info=text_info, count=steps_of_simulation)
simulation.add(World(people))
simulation.add(World(people, ofx = 560))
simulation.run()
