world size: worldXY (xmax, ymax)

people = number of "persons" 


class Person => single person

    random positon: x,y
    dynamic infection: status vector 0-9 (5 = infection, red color)
    time of inf. red -> yellow
    ...
    
    
class World => all persons 

class Simulation - main loop

   
<img src="https://github.com/octopusengine/epidemic_simulator/blob/master/simul_10_3_5.png" width = 600> 


threshold_resistance: 
   30 => 30% of population is completely resistant 
   (blue color)


dist_infect = Distance infection (purple circle)


bmax = Brownian motion + / - (orange square) 
   
   random motion: +/-x,+/-y




not infected

asymptomatic

infected

symptomatic infected

critical condition

recovered 

recovered a resistant

