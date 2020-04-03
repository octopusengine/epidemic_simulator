Prepare:
<code>pip install pygame</code>
or <code>python -m pip install pygame</code>
or <code>pip3 ...</code>


world size: worldXY (xmax, ymax)

people = the total number of people in the simulated environment (default 1000, try 500, 1000, 2000)

class Person => single person

    random positon: x,y
    dynamic infection: status vector 0-9 (5 = infection, red color)
    time of infection: red (7 day) -> yellow (30 days) -> green     
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
   10 => 10% of population is completely resistant (try 10,20,30,40,50,60)
   

::::::::::...........

