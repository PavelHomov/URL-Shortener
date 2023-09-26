from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .error_handlers import (
    InvalidAPIUsage,
    ShortIsBadException,
    ShortIsExistsException,
)
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Фунция добавления ссылки."""
    data = request.get_json(silent=True)
    try:
        long_url = data['url']
    except TypeError:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    except KeyError:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short = data.get('custom_id')
    try:
        link_record = URLMap().short_creator(long_url, short, do_validate=True)
    except ShortIsExistsException:
        raise InvalidAPIUsage(f'Имя "{short}" уже занято.')
    except ShortIsBadException:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    return jsonify(dict(
        url=long_url,
        short_link=url_for(
            'redirect_view',
            link=link_record.short,
            _external=True
        ),
    )), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_link(short_id):
    """Фунция получения ссылки."""
    link = URLMap.get(short_id)
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK
