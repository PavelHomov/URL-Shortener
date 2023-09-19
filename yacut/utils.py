from random import choices
from re import match
from string import ascii_letters, digits

from .constants import PATTERN, SHORT_ID_SYM
from .models import URLMap


def get_unique_short_id():
    """Получить случайное short id."""
    while True:
        short_id = ''.join(choices(ascii_letters + digits, k=SHORT_ID_SYM))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def correct_short(short):
    """Сравнение ссылки с шаблоном."""
    return bool(match(PATTERN, short))
