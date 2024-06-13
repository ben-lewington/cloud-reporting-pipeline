from typing import Callable
from environment import env

REQUIRED_VARS = [
    "username",
    "password",
    "host",
    "port",
    "database",
]


def env_database_connection_str(prefix: str, visit_var: Callable[[str], str] | None = None) -> str:
    vv = visit_var or str.upper
    var_names = tuple(vv(f'{prefix}_{x}') for x in REQUIRED_VARS)

    return 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(*env(*var_names))
