import re
from http import HTTPStatus
from urllib.parse import urljoin

from flask import jsonify, request
from flask.wrappers import Response

from yacut import app, db
from yacut.constants_messages import (BASE_URL, BODY_ERR, SHORT_ID_LENGTH,
                                      SHORT_URL_PATTERN, SHORT_URL_FIELD_ERR,
                                      WRONG_ID_ERR, URL_FIELD_REQUIRED_ERR,
                                      URL_EXISTS_ERR)
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import check_short_id_in_db, get_unique_short_id, save_in_db


@app.route('/api/id/', methods=('POST',))
def get_short_url() -> tuple[Response, int]:
    """Создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(BODY_ERR)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_FIELD_REQUIRED_ERR)
    if 'custom_id' not in data or not data['custom_id']:
        data['custom_id'] = get_unique_short_id(SHORT_ID_LENGTH)
    if check_short_id_in_db(data['custom_id']):
        raise InvalidAPIUsage(URL_EXISTS_ERR)
    if not re.search(SHORT_URL_PATTERN, data['custom_id']):
        raise InvalidAPIUsage(SHORT_URL_FIELD_ERR)
    url_map = URLMap()
    url_map.from_dict(data)
    save_in_db(url_map)
    result_url = url_map.original
    result_short_url = urljoin(BASE_URL, url_map.short)
    return (jsonify({'short_link': result_short_url, 'url': result_url}),
            HTTPStatus.CREATED)


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_url(short_id: str) -> tuple[Response, int]:
    """Получение оригинальной ссылки по указанному короткому идентификатору."""
    origin_url = URLMap.query.filter_by(short=short_id).first()
    if origin_url is None:
        raise InvalidAPIUsage(WRONG_ID_ERR, HTTPStatus.NOT_FOUND)
    return jsonify({'url': origin_url.original}), HTTPStatus.OK
