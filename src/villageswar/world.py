from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import filter
from builtins import range
from builtins import int
from future import standard_library
standard_library.install_aliases()

from builtins import object
from villageswar.action import action_map, ATTACK_ACTION, \
    PROCREATE_ACTION, HEAL_ACTION, GUARD_ACTION, DISTRACT_ACTION, \
    PLAY_WOODS_ACTION, REST_ACTION, PLAY_ACTION
from villageswar.config import get_config, get_cmd_args, stop
from villageswar.information import info
from random import choice, uniform, randint

# Gets the selected configuration

config = get_config()


def maximum(val, max_val):
    if val > max_val:
        return max_val
    else:
        return val


# Class representing the simulated world and its time passing

def process_action(villager, categories, village_1_2, villager_index, rem_indexes):
    village_map = {True: 0, False: 1}
    ally_village = village_map[village_1_2]
    enemy_village = village_map[not village_1_2]
    
    # Processes the action passing the villager (and a target, if it has) to the correct function
    
    # Checks if villager died, and, if yes, indicates its removal
    
    if not villager.alive:
        return villager_index,
    
    if villager.action.action_type == ATTACK_ACTION:
        
        # Calculates infiltration chance
        
        presence_modifier = config['action-extra']['guard-presence-modifier']
        
        infiltration_chance = (1 - presence_modifier) ** len(categories[enemy_village][GUARD_ACTION])
        infiltrate = uniform(0, 1) <= infiltration_chance
        
        if infiltrate:
            # If infiltrated, everyone resting and also healers, breeders and children are in danger
            
            prone_to_attack = categories[enemy_village][REST_ACTION] \
                              + categories[enemy_village][PROCREATE_ACTION] \
                              + categories[enemy_village][PLAY_ACTION] \
                              + categories[enemy_village][HEAL_ACTION]
        else:
            # If not, only kids playing the woods, warriors in guard and distracted ones are endangered
            
            prone_to_attack = categories[enemy_village][GUARD_ACTION] \
                              + categories[enemy_village][DISTRACT_ACTION] \
                              + categories[enemy_village][PLAY_WOODS_ACTION]
        
        # Nobody to attack
        
        if not len(prone_to_attack):
            return villager_index,
        
        target_index = choice(range(len(prone_to_attack)))
        target = prone_to_attack[target_index]
        
        return process_combat(villager, target, target.action.action_type != GUARD_ACTION,
                              villager_index, target_index)
    
    elif villager.action.action_type == PROCREATE_ACTION and not villager.pregnant:
        opposite_sex = {'male': 'female', 'female': 'male'}
        
        # Filter indexes of all villagers of the opposite sex, index is used later for pop()
        
        possible_partners = list(filter(lambda x:
                                        categories[ally_village][PROCREATE_ACTION][x].sex
                                        == opposite_sex[villager.sex]
                                        and not
                                        categories[ally_village][PROCREATE_ACTION][x].pregnant
                                        and x not in rem_indexes,
                                        range(0,
                                              len(categories[ally_village][PROCREATE_ACTION]))))
        # Nobody to be partner
        
        if not len(possible_partners):
            return villager_index,
        
        partner_index = choice(possible_partners)
        partner = categories[ally_village][PROCREATE_ACTION][partner_index]
        
        # Puts both villagers on REST after procreating
        
        indexes = process_procreating(villager, partner, villager_index, partner_index)
        
        return indexes
    elif villager.action.action_type == HEAL_ACTION:
        # Sort villagers by how low the health is
        
        to_cure = categories[ally_village][HEAL_ACTION] + categories[ally_village][REST_ACTION]
        
        # Nobody is left to cure
        
        if not len(to_cure):
            return villager_index,
        
        possible_patients = sorted(to_cure, key=lambda v: v.actual_health)
        patient = possible_patients[0]
        return process_healing(villager, patient, villager_index)
    
    return ()


def process_combat(villager1, villager2, target_off_guard, villager_index, target_index):
    # Simulates a combat between the attacker and the target
    
    info('%s attacks %s' % (villager1, villager2),
         village=villager1.village.name)
    
    not_flee_chance = 1 - config['action-extra']['flee-chance']
    resistance_effect = config['action-extra']['resistance-effect']
    off_guard_penalty = config['action-extra']['off-guard-penalty']
    turns = 0
    
    # Runs loop while there's no fleeing
    # If target is baby, can't flee
    
    # When one or both villagers die, fight is over
    
    while True:
        if not villager1.alive or not villager2.alive:
            break
        
        turns += 1
        
        # Calculates flee chance
        
        if uniform(0, 1) > (1 - not_flee_chance ** turns) and not villager2.baby:
            # Target fled, fight is over
            break
        
        # Villager 1 attacks
        
        if randint(0, 100) <= villager1.actual_accuracy and villager1.alive:

            target_resistance = villager2.actual_resistance
            
            if target_off_guard:
                # Applies off-guard penalty
                
                target_resistance *= 1 - off_guard_penalty
                target_resistance = int(target_resistance)
            
            # Calculates damage
            
            dmg = villager1.actual_strength
            dmg *= ((1 - resistance_effect) ** target_resistance)
            dmg = int(dmg)
            
            # Applies damage
            
            villager2.lose_health(dmg)
        
        if randint(0, 100) <= villager2.actual_accuracy and villager2.alive:

            # If villager is baby, can't do anything
            
            if not villager2.baby:
                # Calculates damage
                
                dmg = villager2.actual_strength
                dmg *= ((1 - resistance_effect) ** villager1.actual_resistance)
                dmg = int(dmg)
                
                # Applies damage
                
                villager1.lose_health(dmg)
    
    return villager_index, target_index


def process_procreating(villager1, villager2, villager_index, partner_index):
    # Simulates procreating between partners
    
    info('%s procreates with %s' % (villager1, villager2),
         village=villager1.village.name)
    
    # If one is sterile, not happening
    if villager1.fertility == 0:
        return villager_index,
    if villager2.fertility == 0:
        return partner_index,
    
    # Gets the average fertility based on both villagers
    
    avg_fertility = (villager1.fertility + villager2.fertility) / 2
    
    chance_reduction = config['jobs']['breeder']['multiple-babies-chance-reduction']
    max_children = config['jobs']['breeder']['maximum-children-per-pregnancy']
    children = []
    stat_range = [1 - config['base-stats']['stat-variation'], 1 + config['base-stats']['stat-variation']]
    
    # Tries fertilization
    
    for i in range(0, max_children):
        if uniform(0, 1) <= avg_fertility * (chance_reduction ** i):
            # Success
            baby_sex = choice(('male', 'female'))
            sex = {'male': 'man', 'female': 'woman'}[baby_sex]
            max_var = config['base-stats']['stat-variation'] + 1
            
            children.append(({
                                 'health': maximum(
                                     int((villager1.base_health + villager2.base_health) / 2 * uniform(*stat_range)),
                                     int(config['base-stats'][sex]['health'] * max_var)),
                                 'strength': maximum(
                                     int((villager1.base_strength + villager2.base_strength) / 2
                                         * uniform(*stat_range)),
                                     int(config['base-stats'][sex]['strength'] * max_var)),
                                 'resistance': maximum(
                                     int((villager1.base_resistance + villager2.base_resistance) / 2
                                         * uniform(*stat_range)),
                                     int(config['base-stats'][sex]['resistance'] * max_var)),
                                 'intelligence': maximum(
                                     int((villager1.base_intelligence + villager2.base_intelligence) / 2
                                         * uniform(*stat_range)),
                                     int(config['base-stats'][sex]['intelligence'] * max_var)),
                                 'accuracy': maximum((villager1.base_accuracy + villager2.base_accuracy) / 2,
                                                     config['base-stats']['base-accuracy'] * max_var)
                             }, baby_sex))
    
    # Sets the baby data on the female villager
    
    if villager1.sex == 'female':
        villager1.pregnant = True
        villager1.pregnant_time = 0
        villager1.children_pregnant = children
    else:
        villager2.pregnant = True
        villager2.pregnant_time = 0
        villager2.children_pregnant = children
    
    return villager_index, partner_index


def process_healing(villager1, villager2, villager_index):
    # Simulates a healing made by the healer on other villager
    
    info('%s heals %s' % (villager1, villager2),
         village=villager1.village.name)
    
    # Calculates the amount to be healed
    
    healing_amount = config['jobs']['healer']['healing-base'] * villager1.actual_intelligence
    
    if (villager2.actual_health + healing_amount) > villager2.health:
        # If healing more than health, health becomes full instead
        
        villager2.actual_health = villager2.health
    else:
        # Otherwise, heals the patient by the amount
        
        villager2.actual_health += healing_amount
    
    return villager_index,


class World(object):
    def __init__(self, village1, village2):
        # Initializes with both village instances
        
        self.name = config['world-name']
        self.village1 = village1
        self.village2 = village2
        self.date = {
            'day': 1,
            'year': 0,
            'days': 0
        }
    
    def date_formatted(self):
        return '%s - Day: %d   Year: %d' % (self.name, self.date['day'], self.date['year'])
    
    def day_pass(self):
        # Simulates a day passed in the world
        
        info('DAY: %d  YEAR: %d' % (self.date['day'], self.date['year']), village=self.name)
        
        # Day start
        
        self.village1.day_start()
        self.village2.day_start()
        
        # Resolves every action
        
        for i in range(config['action-extra']['actions-per-day']):
            self.resolve_actions()
            self.village1.remove_dead()
            self.village2.remove_dead()
        
        # Day end
        
        self.village1.day_end()
        self.village2.day_end()
        self.date_update()
        
        # Checks if day limit reached
        
        cmd_args = get_cmd_args()
        
        if 'until' in cmd_args:
            if self.date['days'] >= cmd_args['until']:
                # Stops the simulation
                
                stop()
        
    def resolve_actions(self):
        # Resolves the actions
        
        categories = self.get_action_categories()
        
        # Will store indexes to be removed after action
        
        removal_indexes = ([], [])
        
        # Processes each action list by category
        
        # Processes village 1
        
        for k, v in categories[0].items():
            for index, i in enumerate(v):
                removal = process_action(i, categories, True, index, removal_indexes[0])
                
                for j in removal:
                    removal_indexes[0].append(j)
            
            categories[0][k] = [value for index, value in enumerate(v) if index not in removal_indexes[0]]
        
        # Processes village 2
        
        for k, v in categories[1].items():
            for index, i in enumerate(v):
                removal = process_action(i, categories, False, index, removal_indexes[1])
                
                for j in removal:
                    removal_indexes[1].append(j)
            
            categories[1][k] = [value for index, value in enumerate(v) if index not in removal_indexes[1]]
    
    def get_action_categories(self):
        # Separates all villagers into lists of actions
        
        actions = list(action_map.values())
        categories = ({}, {})
        
        for i in actions:
            categories[0][i] = []
            categories[1][i] = []
        
        # Gets all villagers in one single list
        
        # Iterates over villagers in order to classify them
        
        # Iterates over village 1 population
        
        for i in self.village1.population:
            categories[0][i.action.action_type].append(i)
        
        # Iterates over village 2 population
        
        for i in self.village2.population:
            categories[1][i.action.action_type].append(i)
        
        return categories
    
    def date_update(self):
        # Updates the age of the world
        
        self.date['days'] += 1
        
        # Checks if an year has passed
        
        if self.date['day'] == config['time']['year']:
            # Updates to next year
            
            self.date['year'] += 1
            self.date['day'] = 1
        else:
            # Otherwise, updates to next day
            
            self.date['day'] += 1
