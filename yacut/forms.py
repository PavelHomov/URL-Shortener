from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    URL,
    DataRequired,
    Length,
    Optional,
    ValidationError,
)

from .constants import SHORT_ID_VALID_MAX, SHORT_ID_VALID_MIN
from .models import URLMap


class LinkForm(FlaskForm):
    """Форма для ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(SHORT_ID_VALID_MIN, SHORT_ID_VALID_MAX), Optional()
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        """Валидация кастомного айди."""
        if URLMap.get(field.data):
            raise ValidationError(
                f'Имя {field.data} уже занято!'
            )
