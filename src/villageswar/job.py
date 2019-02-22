from random import uniform
from villageswar.config import get_config


# Gets configuration

config = get_config()


def mk_warrior():
    # Wrapper to later declared class
    
    return Warrior()


def mk_breeder():
    # Wrapper to later declared class
    
    return Breeder()


def mk_healer():
    # Wrapper to later declared class
    
    return Healer()


# Job base class

class Job(object):
    # Dictionary of job names
    jobs = {
        config['jobs']['names'][0]: mk_warrior,
        config['jobs']['names'][1]: mk_breeder,
        config['jobs']['names'][2]: mk_healer
    }
    
    def __init__(self):
        # Initializes job data
        
        self.years = 0
        self.professional = False
    
    def year_service(self):
        # Simulates a year of service
        
        self.years += 1
        
        # Checks if villager not yet a professional
        
        if not self.professional:
            professional_time = config['jobs']['professional-minimum-time']
            
            # If not and has enough years of service, tries luck to become professional
            
            if self.years >= professional_time:
                chance = self.calculate_professional_chance()
                rand = uniform(0, 1)
                
                if rand <= chance:
                    self.professional = True
    
    def calculate_professional_chance(self):
        # Calculates the chance of becoming professional at the job
        
        multiplier = config['jobs']['professional-multiplier'] \
                     ** (1 + self.years - config['jobs']['professional-minimum-time'])
        
        chance = 1 - multiplier + config['jobs']['professional-chance-base'] * multiplier
        
        return chance
    
    def get_job_multiplier(self):
        # Returns stat multiplier of job
        
        return NotImplemented
    
    @classmethod
    def get_job(cls, name):
        # Returns the wrapper for job constructor based on the name
        
        return cls.jobs[name]()
    
    def __repr__(self):
        return '%s%s: %i years' \
               % (type(self).__name__, {True: ' (Professional)', False: ''}[self.professional], self.years)


# The Warrior job class

class Warrior(Job):
    # Name identifier for job
    
    name = config['jobs']['names'][0]
    
    def __init__(self):
        # Initializes parent class
        
        super().__init__()
    
    def get_job_multiplier(self):
        # Returns stat multiplier of job
        
        technique = config['jobs']['warrior']['technique-multiplier']
        
        if self.professional:
            technique *= config['jobs']['professional-multiplier']
        
        return {
            'strength': technique,
            'resistance': technique
        }


# The Breeder job class

class Breeder(Job):
    # Name identifier for job
    
    name = config['jobs']['names'][1]
    
    def __init__(self):
        # Initializes parent class
        
        # noinspection PySuperArguments
        super().__init__()
    
    def get_job_multiplier(self):
        # Returns stat multiplier of job
        
        fertility_bonus = config['jobs']['breeder']['fertility-multiplier']
        
        if self.professional:
            fertility_bonus *= config['jobs']['professional-multiplier']
        
        return {
            'fertility': fertility_bonus
        }


# The Healer job class

class Healer(Job):
    # Name identifier for job
    
    name = config['jobs']['names'][2]
    
    def __init__(self):
        # Initializes parent class
        
        super().__init__()
    
    def get_job_multiplier(self):
        # Returns stat multiplier of job
        
        return {}
