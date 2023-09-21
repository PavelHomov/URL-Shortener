from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import validate_create_id, database_save


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Фунция добавления ссылки."""
    data = request.get_json()
    validate_create_id(data)
    link = URLMap()
    link.from_dict(data)
    database_save(link)
    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_link(short_id):
    """Фунция получения ссылки."""
    link = URLMap.get(short_id)
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK
