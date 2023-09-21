from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import LinkForm
from .models import URLMap
from .utils import get_unique_short_id, database_save


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Вью функция главной страницы."""
    form = LinkForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        elif URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('main.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        database_save(url_map)
        flash(f'Ваша новая ссылка готова: '
              f'<a href="{request.base_url}{custom_id}">'
              f'{request.base_url}{custom_id}</a>')
    return render_template('main.html', form=form)


@app.route('/<path:link>')
def redirect_view(link):
    """Вью функция редиректа."""
    link_database = URLMap.get(link)
    if link_database is None:
        abort(404)
    return redirect(link_database.original)
