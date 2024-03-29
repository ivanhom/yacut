from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Optional, Regexp, URL

from yacut.constants_messages import (CREATE_BUTTON, CUSTOM_URL_LABEL,
                                      LONG_URL_LABEL, REQUIRED_FIELD_ERR,
                                      WRONG_URL_ERR, SHORT_URL_PATTERN,
                                      WRONG_SHORT_URL_ERR)


class URLForm(FlaskForm):
    """Описание полей формы для записи в БД."""
    original_link = URLField(
        LONG_URL_LABEL,
        validators=(DataRequired(message=REQUIRED_FIELD_ERR),
                    URL(message=WRONG_URL_ERR))
    )
    custom_id = URLField(
        CUSTOM_URL_LABEL,
        validators=(Regexp(SHORT_URL_PATTERN, message=WRONG_SHORT_URL_ERR),
                    Optional())
    )
    submit = SubmitField(CREATE_BUTTON)
