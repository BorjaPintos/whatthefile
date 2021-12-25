import platform

from src.domain.enumso import SO

BOOLEAN_STATES = {
    '1': True,
    'si': True,
    'yes': True,
    'true': True,
    'on': True,
    '0': False,
    'no': False,
    'false': False,
    'off': False,
}

PLATFORMS = {
    'Linux': SO.LINUX,
    'Windows': SO.WINDOWS,
    'Darwin': SO.MACOS
}


def convert_to_boolean(value):
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        if value.lower() not in BOOLEAN_STATES:
            return False
        return BOOLEAN_STATES[value.lower()]
    else:
        return False


def get_SO():
    name = platform.system()
    if name not in PLATFORMS:
        return None
    return PLATFORMS[name]
