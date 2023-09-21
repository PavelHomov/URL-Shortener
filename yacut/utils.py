from http import HTTPStatus
from random import choices
from yacut import db
from re import match
from string import ascii_letters, digits

from .constants import PATTERN, SHORT_ID_SYM, SHORT_ID_VALID_MAX
from .error_handlers import InvalidAPIUsage
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


def validate_create_id(data):
    """Фунция валидации данных."""
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if data.get('custom_id'):
        if len(data['custom_id']) > SHORT_ID_VALID_MAX or not correct_short(
                data['custom_id']
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                status_code=HTTPStatus.BAD_REQUEST,
            )
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    else:
        data['custom_id'] = get_unique_short_id()


def database_save(model):
    db.session.add(model)
    db.session.commit()
