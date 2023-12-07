from flask import abort, flash, redirect, render_template, url_for

from . import app
from .error_handlers import URLMapException
from .forms import LinkForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Вью функция главной страницы."""
    form = LinkForm()
    if not form.validate_on_submit():
        return render_template('main.html', form=form)
    original_link = form.original_link.data
    short_link = form.custom_id.data
    try:
        link_record = URLMap().short_creator(
            original_link, short_link
        )
    except URLMapException:
        flash(f'Имя {short_link} уже занято!')
        return render_template('main.html', form=form)
    full_short_link = url_for(
        'redirect_view', link=link_record.short, _external=True
    )
    return render_template(
        'main.html',
        form=form,
        full_short_link=full_short_link,
    )


@app.route('/<path:link>')
def redirect_view(link):
    """Вью функция редиректа."""
    link_database = URLMap.get(link)
    if link_database is None:
        abort(404)
    return redirect(link_database.original)
