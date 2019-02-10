from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

from builtins import object
from villageswar.villager import Villager
from villageswar.information import info


# Class representing a village

class Village(object):
    def __init__(self, name):
        # Initializes an empty population
        
        self.population = []
        self.name = name
        self.data = {
            'dead': 0,
            'days': 0
        }
    
    def day_start(self):
        # Simulates the start of a day in the village
        
        # Iterates over population in order to call their methods
        
        self.data['days'] += 1
    
    def population_activities(self):
        for i in self.population:
            i.choose_action()
    
    def day_end(self):
        # Simulates the end of a day in the village
        
        # Iterates over population in order to call their methods
        
        for i in self.population:
            i.day_end()
            
    def remove_dead(self):
        # Clears dead villagers from list
    
        for i in self.population:
            if not i.alive:
                self.population.remove(i)
                self.data['dead'] += 1
    
    def birth(self, baby_stats):
        baby = Villager(baby_stats[1], self, parent_stats=baby_stats[0])
        self.population.append(baby)
        info('%s was born' % baby, village=self.name)
    
    def __repr__(self):
        return self.name
