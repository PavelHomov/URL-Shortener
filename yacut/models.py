from datetime import datetime
from random import choices
from re import fullmatch
from string import ascii_letters, digits

from yacut import db
from yacut.constants import SHORT_ID_VALID_MAX, SHORT_ID_SYM, PATTERN, ORIGINAL_LINK_LENGTH
from yacut.error_handlers import (
    ShortIsBadException,
    ShortIsExistsException,
    URLMapException,
)


class URLMap(db.Model):
    """Модель ссылки."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(
        db.String(SHORT_ID_VALID_MAX),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short_link):
        """Получить объект модели."""
        return URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def short_validator(short):
        """Валидация короткой ссылки."""
        if len(short) > SHORT_ID_VALID_MAX:
            raise ShortIsBadException('Не соответствует разрешенной длине!')
        if not fullmatch(PATTERN, short):
            raise ShortIsBadException('Использованы запрещенные символы!')
        if URLMap.get(short):
            raise ShortIsExistsException('Такое имя уже существует!')
        return short

    @staticmethod
    def short_link_generator():
        """Получить случайное short id."""
        while True:
            short_id = ''.join(choices(ascii_letters + digits, k=SHORT_ID_SYM))
            if not URLMap.get(short_id):
                return short_id

    @staticmethod
    def short_creator(original_link, short, do_validate=False):
        """Если валидация пройдена, происходит сохранение в БД."""
        if do_validate and (len(original_link) > ORIGINAL_LINK_LENGTH):
            raise URLMapException('Ссылка первышает допустимый размер!')
        if not short:
            short = URLMap.short_link_generator()
        elif do_validate:
            URLMap.short_validator(short)
        url_map = URLMap(
            original=original_link,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
