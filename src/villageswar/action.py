from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# Action unique type identifiers

from future import standard_library

standard_library.install_aliases()
from builtins import object


# Action strings

REST_ACTION = 'REST_ACTION'
PLAY_ACTION = 'PLAY_ACTION'
PLAY_WOODS_ACTION = 'PLAY_WOODS'
ATTACK_ACTION = 'ATTACK_ACTION'
GUARD_ACTION = 'GUARD_ACTION'
PROCREATE_ACTION = 'PROCREATE_ACTION'
HEAL_ACTION = 'HEAL_ACTION'
DISTRACT_ACTION = 'DISTRACT_ACTION'


# Represents a queued action

class Action(object):
    def __init__(self, action_type):
        self.action_type = action_type
    
    def __repr__(self):
        return self.action_type


# Maps selected action to action unique type identifier

action_map = {
    'rest': REST_ACTION,
    'play': PLAY_ACTION,
    'play-woods': PLAY_WOODS_ACTION,
    'attack': ATTACK_ACTION,
    'guard': GUARD_ACTION,
    'procreate': PROCREATE_ACTION,
    'heal': HEAL_ACTION,
    'distract': DISTRACT_ACTION
}
