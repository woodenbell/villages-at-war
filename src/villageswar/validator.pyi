def validate_config(json) -> dict: ...

def validate_generator(json) -> dict: ...

def load_config_schema() -> dict: ...

def load_generator_schema() -> dict: ...

config_schema = None # type: dict
generator_schema = None # type: dict