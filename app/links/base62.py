from django.conf import settings

MAX_INDEX = settings.HASH_BASE**settings.TOKEN_LENGTH


def encode(idx: int) -> str:
    _validate_index(idx)

    idx -= 1
    encoded = []
    while idx > 0:
        idx, remainder = divmod(idx, settings.HASH_BASE)
        encoded.append(settings.SECRET_HASH_KEY[remainder])
    return ''.join(reversed(encoded)).rjust(
        settings.TOKEN_LENGTH, settings.SECRET_HASH_KEY[0]
    )


def decode(token: str) -> int:
    decoded = 0
    for char in token:
        decoded = decoded * settings.HASH_BASE + settings.SECRET_HASH_KEY.index(char)

    return decoded + 1


def _validate_index(idx: int):
    if idx <= 0:
        raise ValueError('The index must be greater than 0.')
    elif idx > MAX_INDEX:
        raise ValueError('The index is out of range.')
