class InvalidConfigError(Exception):
    ...

    def __init__(self, msg):
        ...

class InvalidGeneratorError(Exception):
    ...

    def __init__(self, msg):
        ...

class SimulationError(Exception):
    ...

    def __init__(self, msg, cause):
        ...
