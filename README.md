world size: worldXY (xmax, ymax)

people = the total number of people in the simulated environment (default 1000)

class Person => single person

    random positon: x,y
    dynamic infection: status vector 0-9 (5 = infection, red color)
    time of inf. red -> yellow
    ...
    
    
class World => all people 

class Simulation - main loop

   
<img src="https://github.com/octopusengine/epidemic_simulator/blob/master/simul_10_3_5_2.png" width = 600> 

dist_infect = Distance infection (purple circle)

brown_mov_max = Brownian motion + / - (orange square)  -> random motion: +/-(x), +/-(y)

Person:
* resistant (blue)
* not infected (black)
* infected - asymptomatic (red) 
* symptomatic infected (yellow)
* critical condition (violet)
* recovered (green)
* recovered and resistant (dark green)

.:.

threshold_resistance: 
   30 => 30% of population is completely resistant 
   (blue color)


::::::::::...........

