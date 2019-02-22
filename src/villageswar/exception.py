

# Exceptions to be used

class InvalidConfigError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidGeneratorError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class SimulationError(Exception):
    def __init__(self, msg, cause):
        super().__init__(msg)
        self.cause = cause
