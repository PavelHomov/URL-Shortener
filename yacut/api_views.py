from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import SHORT_ID_VALID_MAX
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import correct_short, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Фунция добавления ссылки."""
    data = request.get_json()
    validate_create_id(data)
    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_link(short_id):
    """Фунция получения ссылки."""
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK


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
