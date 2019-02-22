from typing import Optional, List

from villageswar.action import Action
from villageswar.job import Job
from villageswar.village import Village

config  = None  # type: dict
def age_increase(age): ...

def age_decrease(age): ...

class Villager(object):
    ...

    def __init__(self, sex: str, village: Village, age: int=0, parent_stats: Optional[dict]=None):
        self.id  = None  # type: int
        self.name  = None  # type: str
        self.sex  = None  # type: str
        self.days_counter  = None  # type: int
        self.age  = None  # type: int
        self.alive  = None  # type: bool
        self.baby  = None  # type: bool
        self.adult  = None  # type: bool
        self.retired  = None  # type: bool
        self.village  = None  # type: Village
        self.job  = None  # type: Optional[Job]
        
        self.base_health  = None  # type: int
        self.base_strength  = None  # type: int
        self.base_resistance  = None  # type: int
        self.base_intelligence  = None  # type: int
        self.base_accuracy  = None  # type: int
        
        self.base_fertility  = None  # type: int
        self.health  = None  # type: int
        self.strength  = None  # type: int
        self.resistance  = None  # type: int
        self.fertility  = None  # type: int
        self.intelligence  = None  # type: int
        self.accuracy  = None  # type: int
        self.pregnant  = None  # type: Optional[bool]
        self.pregnant_time  = None  # type: Optional[int]
        self.children_pregnant  = None  # type: Optional[List[(bool, dict)]]
        self.action  = None  # type: Optional[Action]
        self.actual_health  = None  # type: int
        self.actual_strength  = None  # type: int
        self.actual_resistance  = None  # type: int
        self.actual_intelligence  = None  # type: int
        self.actual_accuracy  = None  # type: int
        ...

    def choose_action(self): ...

    def day_end(self): ...

    def pregnancy(self): ...

    def die(self): ...

    def lose_health(self, amount: int): ...

    def calculate_death_chance(self) -> float: ...

    def mortality_risk(self): ...

    def calculate_stats(self): ...

    def check_fertility(self): ...

    def actual_stats(self): ...

    def grow_up(self): ...

    def job_selection(self): ...

    def age_modifier(self) -> float: ...

    def info(self) -> str: ...

    def __repr__(self) -> str: ...
