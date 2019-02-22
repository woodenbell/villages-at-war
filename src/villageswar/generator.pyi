from typing import List, Union

from villageswar.village import Village

config = None # type:
class Generator(object):
    ...

    def __init__(self, generator: dict):
        self.g1 = None  # type: List[GeneratorStatement]
        self.g2 = None  # type: List[GeneratorStatement]
        ...

    def generate(self, village1: Village, village2: Village): ...

class GeneratorStatement(object):
    ...

    def __init__(self, amount: Union[int, List[int]], sex: Union[str, List[int]]=None, job: Union[str, List[int]]=None,
                 age: Union[int, List[Union[int, List[Union[int, List[int]]]]]]=None):
        self.amount = None  # type: Union[int, List[int]]
        self.sex = None  # type: Union[str, List[int]]
        self.job = None  # type: Union[str, List[int]]
        self.age = None  # type: Union[int, List[Union[int, List[Union[int, List[int]]]]]]
        ...

    def generate(self, village: Village): ...

    def generate_list(self) -> List[dict]: ...

def separate_by_percentage(l: list, percentage: List[int]) -> List[list]: ...
