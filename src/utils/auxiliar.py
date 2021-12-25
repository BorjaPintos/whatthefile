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


def get_str_utf_8_from_bytes(binary_bytes: bytes) -> str:

    types = ["utf-8","latin-1",  "utf-16", "utf-32", "mbcs"]
    for tipo in types:
        try:
            return binary_bytes.decode(tipo)
        except:
            pass
            "try next type"

    return None
