from urllib.parse import urljoin

from flask import flash, redirect, render_template, request
from werkzeug.wrappers import Response

from yacut import app, db
from yacut.constants_messages import (SHORT_ID_LENGTH, URL_CREATED,
                                      URL_EXISTS_ERR)
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import check_short_id_in_db, get_unique_short_id, save_in_db


@app.route('/', methods=('GET', 'POST'))
def index_view() -> str:
    """Генерация коротких ссылок и связь их с исходными длинными ссылками."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_id = form.custom_id.data

    if short_id:
        if check_short_id_in_db(short_id):
            flash(URL_EXISTS_ERR, category='error')
            return render_template('index.html', form=form)
    else:
        short_id = get_unique_short_id(SHORT_ID_LENGTH)
    short_url = urljoin(request.base_url, short_id)

    url_map = URLMap(original=form.original_link.data, short=short_id)
    save_in_db(url_map)
    flash(URL_CREATED, category='success')
    flash(short_url, category='url')
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def original_url_view(short_id: str) -> Response:
    """Переадресация на исходный адрес при обращении к коротким ссылкам."""
    origin_url = URLMap.query.filter_by(short=short_id).first_or_404().original
    return redirect(origin_url)
