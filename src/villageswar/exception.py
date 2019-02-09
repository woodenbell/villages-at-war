from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()


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
