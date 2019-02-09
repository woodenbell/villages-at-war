from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import range
from builtins import int
from future import standard_library
standard_library.install_aliases()

from builtins import object
from functools import reduce
from random import choice, randint, uniform
from villageswar.config import get_config, next_id
from villageswar.information import info
from villageswar.action import action_map, Action

# Gets the selected configuration
from villageswar.job import Job

config = get_config()


def age_increase(age):
    # Calculates stat increase modifier based on age
    
    return (age * config['age']['increase']) ** 2


def age_decrease(age):
    # Calculates stat decrease modifier based on age
    
    return ((age - config['age']['apex']) * config['age']['decrease']) ** 2


# Villager base class

class Villager(object):
    def __init__(self, sex, village, age=0, parent_stats=None):
        # Calculates all base stats based on margin and further stats
        
        sex_map = {'male': 'man', 'female': 'woman'}
        
        # Picks random name based on sex
        
        self.id = next_id()
        self.name = choice([*config['names'][sex_map[sex]], *config['names']['gender-neutral']])
        self.sex = sex
        self.days_counter = 0
        self.age = age
        self.alive = True
        self.baby = age <= config['age']['baby']
        self.adult = age >= config['age']['adulthood']
        self.retired = age >= config['age']['retirement']
        self.village = village
        self.job = None
        stat_range = [1 - config['base-stats']['stat-variation'], 1 + config['base-stats']['stat-variation']]
        
        if parent_stats is None:
            # If no parents (generated) use config for base
            
            self.base_health = int(config['base-stats'][sex_map[self.sex]]['health'] * uniform(*stat_range))
            self.base_strength = int(config['base-stats'][sex_map[self.sex]]['strength'] * uniform(*stat_range))
            self.base_resistance = int(config['base-stats'][sex_map[self.sex]]['resistance'] * uniform(*stat_range))
            self.base_intelligence = int(config['base-stats'][sex_map[self.sex]]['intelligence'] * uniform(*stat_range))
            self.base_accuracy = config['base-stats']['base-accuracy']
        else:
            # If has parents, use their stats
            
            self.base_health = parent_stats['health']
            self.base_strength = parent_stats['strength']
            self.base_resistance = parent_stats['resistance']
            self.base_intelligence = parent_stats['intelligence']
            self.base_accuracy = parent_stats['accuracy']
        
        self.base_fertility = None
        self.health = None
        self.strength = None
        self.resistance = None
        self.fertility = None
        self.intelligence = None
        self.accuracy = None
        self.pregnant = None
        self.pregnant_time = None
        self.children_pregnant = None
        self.action = None
        self.calculate_stats()
        self.actual_health = self.health
        self.actual_strength = self.strength
        self.actual_resistance = self.resistance
        self.actual_intelligence = self.intelligence
        self.actual_accuracy = self.accuracy
        self.check_fertility()
        self.actual_stats()
    
    def day_start(self):
        # Simulates the start of a day in the life of the villager
        
        # If dead, do nothing
        
        if not self.alive:
            return
        
        # Selects an action based on probability and stores it for execution
        
        if self.pregnant:
            category = 'pregnant'
        elif self.retired:
            category = 'retired'
        elif self.adult:
            if not self.job:
                category = 'child'
            elif self.job.__class__.name == config['jobs']['names'][0]:
                category = 'warrior'
            elif self.job.__class__.name == config['jobs']['names'][1]:
                category = 'breeder'
            else:
                category = 'healer'
        elif self.baby:
            category = 'baby'
        else:
            category = 'child'
        
        actions = list(config['action'][category].values())
        action_probabilities = []
        
        for index, i in enumerate(actions):
            action_probabilities.append(i + reduce(lambda a, b: a + b, actions[:i + 1], 0))
        
        # Generates a random number to select the action
        rand_num = randint(0, 100)
        selected = None
        
        for i in range(len(actions)):
            if rand_num <= action_probabilities[i]:
                selected = list(config['action'][category].keys())[i]
                break
        
        self.action = Action(action_map[selected])
    
    def day_end(self):
        # Simulates the end of a day in the life of a villager
        
        self.mortality_risk()
        
        # If dead, do nothing
        
        if not self.alive:
            return
        
        # If pregnant, ages pregnancy
        
        if self.pregnant:
            self.pregnancy()
        
        # Checks if an year has passed
        
        if self.days_counter == config["time"]["year"]:
            # If yes, makes villager grow up
            
            self.grow_up()
            self.days_counter = 0
        else:
            self.days_counter += 1
    
    def pregnancy(self):
        self.pregnant_time += 1
        
        # If enough time has passed, time to give birth
        
        if self.pregnant_time == config['action-extra']['pregnancy-time']:
            for i in self.children_pregnant:
                self.village.birth(i)
            
            self.pregnant = False
            self.pregnant_time = None
            self.children_pregnant = None
    
    def die(self):
        # Makes villager die
        
        info('%s died' % self, village=self.village.name)
        
        self.alive = False
        self.actual_health = 0
    
    def lose_health(self, amount):
        # Reduces health

        self.actual_health -= amount
        
        # Checks if health <= 0 (certain death)
        
        if self.actual_health <= 0:
            # Villager dies
            
            self.die()
        else:
            # Recalculates stats based on lost health
            
            self.actual_stats()
    
    def calculate_death_chance(self):
        
        # Calculates chance of dying
        
        if self.health == 0 or self.actual_health == 0:
            return 1
        
        base_chance = config['death']['base-chance']
        
        health_percentage = self.actual_health / self.health
        
        return 1 - ((1 - base_chance) ** (1 / health_percentage))
    
    def mortality_risk(self):
        # Gets random number to apply risk of dying
        
        rand = uniform(0, 1)
        
        # Tests against chance of dying

        if rand <= self.calculate_death_chance() and not self.alive:
            # Makes villager die
            
            self.die()
    
    def calculate_stats(self):
        # Calculates maximum stats based on base stats
        
        # Gets age modifier
        
        modifier = self.age_modifier()
        previous_health = None
        
        # Used to apply health change to actual
        
        if self.health is not None:
            previous_health = self.health
        
        # Calculates stats based on modifier
        
        self.health = int(self.base_health * modifier)
        self.strength = int(self.base_strength * modifier)
        self.resistance = int(self.base_resistance * modifier)
        self.intelligence = int(self.base_intelligence * modifier)
        self.accuracy = int(self.base_accuracy * modifier)
        
        # Checks if villager has job and applies its multipliers
        
        if self.job:
            multiplier = self.job.get_job_multiplier()
            
            for k, v in multiplier.items():
                if k == 'health':
                    self.health *= v
                    self.health = int(self.health)
                if k == 'strength':
                    self.strength *= v
                    self.strength = int(self.strength)
                if k == 'resistance':
                    self.resistance *= v
                    self.resistance = int(self.resistance)
                if k == 'intelligence':
                    self.intelligence *= v
                    self.intelligence = int(self.intelligence)
                if k == 'fertility' and self.fertility is not None:
                    self.fertility *= v
        
        # Applies health increase to actual health
        
        if previous_health is not None:
            self.actual_health += self.health - previous_health
        
        # Checks adulthood to introduce fertility stat
        
        if self.adult:
            self.check_fertility()
    
    def check_fertility(self):
        modifier = self.age_modifier()
        
        if self.base_fertility is None:
            self.base_fertility = randint(*config['base-stats']['base-fertility-range'])
            
            # If woman, initializes pregnant stat
            if self.sex == 'female':
                self.pregnant = False
        
        # When old enough, fertility becomes 0
        
        if self.retired:
            self.fertility = 0
        else:
            self.fertility = int(self.base_fertility * modifier)
    
    def actual_stats(self):
        
        # Calculates stats based on how injured the villager is (how low the health is)
        
        # If dead, do nothing to avoid division by 0
        
        if self.actual_health == 0:
            return
        
        influence = config['base-stats']['health-influence']
        missing_percentage = 1 - self.health / self.actual_health
        health_influence = influence * missing_percentage
        
        # Applies the injury penalty based on the influence modifier
        
        self.actual_strength -= health_influence * self.strength
        self.actual_resistance -= health_influence * self.resistance
        self.actual_intelligence -= (health_influence * self.intelligence) / 2
        
        self.actual_accuracy -= health_influence * self.accuracy
        
        self.actual_strength = int(self.actual_strength)
        self.actual_resistance = int(self.actual_resistance)
        self.actual_intelligence = int(self.actual_intelligence)
        self.actual_accuracy = int(self.actual_accuracy)
    
    def grow_up(self):
        
        info('%s grew up (%d years)' % (self, self.age + 1),
             village=self.village.name)
        
        # Simulates growing up and updates stats
        
        self.age += 1
        self.baby = self.age <= config['age']['baby']
        self.adult = self.age >= config['age']['adulthood']
        self.retired = self.age >= config['age']['retirement']
        self.calculate_stats()
        self.actual_stats()
        
        # When reaches adulthood, gets into job selection
        
        if self.adult and not self.retired and self.job is None:
            self.job_selection()
        elif self.adult:
            # If adult, old and has job, time for retirement, otherwise another year of service
            
            if self.job is not None:
                if self.retired:
                    self.job = None
                else:
                    self.job.year_service()
        
        # Calculates mortality risk
        
        self.mortality_risk()
    
    def job_selection(self):
        # Simulates a job selection process
        
        sex_map = {'male': 'man', 'female': 'woman'}
        selected = None
        jobs = config['jobs']['names']
        job_probabilities = []
        
        for i in range(len(jobs)):
            job_probabilities.append(config['jobs']['selection'][sex_map[self.sex]][i]
                                     + reduce(lambda a, b: a + b, job_probabilities[:i + 1], 0))
        
        rand_num = randint(0, 100)
        
        # Selects job based on the probabilities of each sex
        
        for i in range(len(job_probabilities)):
            if rand_num <= job_probabilities[i]:
                selected = jobs[i]
                break
        
        info('%s became %s' % (self, selected), village=self.village.name)
        self.job = Job.get_job(selected)
    
    def age_modifier(self):
        # Calculates age modifier for stats based on the apex age
        
        if self.age < config['age']['apex']:
            return 1 + age_increase(self.age)
        else:
            return 1 + (age_increase(config['age']['apex']) - age_decrease(self.age))
    
    def info(self):
        return ('''Name: %s - Sex: %s - Age: %d
Baby: %s - Adult: %s - Retired: %s
- Job:
%s

- Stats:
Health: %d
Strength: %d
Resistance: %d
Intelligence: %d
Fertility: %d
'''
                % (self.name, {'male': 'M', 'female': 'F'}[self.sex], self.age, self.baby, self.adult, self.retired,
                   self.job, self.actual_health, self.actual_strength, self.actual_resistance,
                   self.actual_intelligence, self.fertility or 0))
    
    def __repr__(self):
        return '%s #%s' % (self.name, self.id)
