import random
import string

from links.models import ShortURL

TOKEN_LENGTH = 6
DOMAIN = 'mini.fy'


def generate_short_link(original_url: str) -> str:
    while True:
        token = _generate_token()
        if not ShortURL.objects.filter(alias=token).exists():
            break

    ShortURL.objects.create(original=original_url, alias=token)
    return f'https://{DOMAIN}/{token}'


def _generate_token(length: int = TOKEN_LENGTH) -> str:
    if length < 1:
        raise ValueError('The length of the random string must be greater than 0.')
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
