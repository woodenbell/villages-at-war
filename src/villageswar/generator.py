from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import range
from builtins import map
from future import standard_library
standard_library.install_aliases()

from builtins import object
from functools import reduce
from random import randint
from villageswar.config import get_config
from villageswar.job import Job
from villageswar.villager import Villager
from villageswar.information import info
from villageswar.exception import InvalidGeneratorError

config = get_config()


# Represents the generator

class Generator(object):
    def __init__(self, generator):
        self.g1 = []
        self.g2 = []
        
        # Separates statements for each village
        
        for i in generator['1']:
            gen_stmt = {}
            
            for j in ('sex', 'job', 'age'):
                if j in i:
                    gen_stmt[j] = i[j]
            
            self.g1.append(GeneratorStatement(i['amount'], **gen_stmt))
        
        for i in generator['2']:
            gen_stmt = {}
            
            for j in ('sex', 'job', 'age'):
                if j in i:
                    gen_stmt[j] = i[j]
            
            self.g2.append(GeneratorStatement(i['amount'], **gen_stmt))
    
    def generate(self, village1, village2):
        # Generates population for each village
        
        for i in self.g1:
            i.generate(village1)
        
        for i in self.g2:
            i.generate(village2)


# Represents each generator statement

class GeneratorStatement(object):
    def __init__(self, amount, sex=None, job=None, age=None):
        self.amount = amount
        self.sex = sex
        self.job = job
        self.age = age
    
    def generate(self, village):
        # Gets generated list and instantiates villagers and to be appended on the village population
        
        to_generate = self.generate_list()
        
        for i in to_generate:
            
            v = Villager(i['sex'], village, age=i['age'])
            
            if 'job' in i:
                v.job = self.job = Job.get_job(i['job'])
                info('Generated %s: %s and %d years old (%s)' % (v, v.sex, v.age, v.job), village='Gen')
            else:
                info('Generated %s: %s and %d years old' % (v, v.sex, v.age), village='Gen')
            
            # Puts the generated villager in the population
            
            village.population.append(v)
    
    def generate_list(self):
        # Generates a list of villager properties based on specified values
        
        if self.amount.__class__ is list:
            if self.amount[0] >= self.amount[1]:
                # Invalid range
                
                raise InvalidGeneratorError('Invalid amount range')
            
            amount = randint(*self.amount)
        else:
            amount = self.amount
        
        villagers = []
        
        for i in range(amount):
            villagers.append({})
        
        if self.sex:
            # Checks whether sex is only one or has proportions
            
            if self.sex.__class__ is str:
                # Translates single sex option into proportion
                
                sex_map = {'male': [100, 0], 'female': [0, 100]}
                sex = sex_map[self.sex]
            else:
                if (self.sex[0] + self.sex[1]) != 100:
                    raise InvalidGeneratorError('Sex proportions do not sum to 100')
                
                sex = self.sex
        else:
            # Separates sex into equal distributions
            
            sex = [50, 50]
        
        # Separates into 2 groups (as the number of groups is limited)
        
        male, female = separate_by_percentage(villagers, sex)
        
        # Sets the sex for each group
        
        for i in male:
            i['sex'] = 'male'
        
        for i in female:
            i['sex'] = 'female'
        
        if self.age:
            # Checks whether age will be defined by a single value or divided in proportions
            
            if self.age.__class__ is int:
                # All villagers will have the defined age
                
                for i in villagers:
                    i['age'] = self.age
            else:
                # Checks whether array is a range or list of proportions
                
                if self.age[0].__class__ is int:
                    if self.age[0] >= self.age[1]:
                        raise InvalidGeneratorError('Invalid age range')
                    
                    for i in villagers:
                        i['age'] = randint(*self.age)
                else:
                    if reduce(lambda a, b: a + b, list(map(lambda x: x[0], self.age))):
                        raise InvalidGeneratorError('Age proportions do not sum into 100')
                    
                    # Separates villagers proportionally
                    
                    age_categories = separate_by_percentage(villagers, list(map(lambda x: x[0], self.age)))
                    
                    for i in range(len(age_categories)):
                        if self.age[i][1].__class__ is int:
                            # If age is defined, sets it
                            
                            for j in age_categories[i]:
                                j['age'] = self.age[i][1]
                        else:
                            # Otherwise, picks a value in range
                            
                            for j in age_categories[i]:
                                j['age'] = randint(*self.age[i][1])
        
        else:
            # Default
            
            age = [0, config['age']['retirement']]
            
            for i in villagers:
                i['age'] = randint(*age)
        
        if self.job:
            # If defined, applies job
            
            if self.job.__class__ is str:
                # If single job defined, set all villagers to that job
                
                for i in villagers:
                    if i['age'] >= config['age']['adulthood']:
                        # If adult, applies job
                        
                        i['job'] = self.job
            else:
                if reduce(lambda a, b: a + b, self.job) != 100:
                    raise InvalidGeneratorError('Job percentages do not sum into 100')
                
                # Separates into three groups (warrior, breeder, healer)
                
                warrior, breeder, healer = separate_by_percentage(villagers, self.job)
                
                # Sets jobs for each category
                
                for i in warrior:
                    i['job'] = 'warrior'
                
                for i in breeder:
                    i['job'] = 'breeder'
                
                for i in healer:
                    i['job'] = 'healer'
        else:
            
            # Separates equally
            
            warrior, breeder, healer = separate_by_percentage(villagers, [33, 33, 34])
            
            for i in warrior:
                i['job'] = 'warrior'
            
            for i in breeder:
                i['job'] = 'breeder'
            
            for i in healer:
                i['job'] = 'healer'
        
        return villagers


def separate_by_percentage(l, percentage):
    # Separates list into distributions based on percentage
    
    total_len = len(l)
    total_percentages = []
    result = []
    
    for i in range(len(percentage)):
        result.append([])
    
    for i in range(len(percentage)):
        total_percentages.append(reduce(lambda a, b: a + b, percentage[:i + 1], 0))
    
    for i in range(len(l)):
        for j in range(len(total_percentages)):
            if i <= (total_percentages[j] / 100) * total_len:
                result[j].append(l[i])
                break
    
    return result
