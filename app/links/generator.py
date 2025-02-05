import random
import string

from django.conf import settings


def generate_token(idx: int) -> str:
    if settings.TOKEN_LENGTH < 1:
        raise ValueError('The length of the token must be greater than 0.')
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=settings.TOKEN_LENGTH)
    )
