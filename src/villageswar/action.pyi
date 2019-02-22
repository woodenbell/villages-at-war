from typing import Dict

REST_ACTION = None # type: str
PLAY_ACTION = None # type: str
PLAY_WOODS_ACTION = None # type: str
ATTACK_ACTION = None # type: str
GUARD_ACTION = None # type: str
PROCREATE_ACTION = None # type: str
HEAL_ACTION = None # type: str
DISTRACT_ACTION = None # type: str

class Action(object):
    ...

    def __init__(self, action_type: str):
        self.action_type = None # type: str
        ...

    def __repr__(self) -> str: ...

action_map = None # type: Dict[str, str]