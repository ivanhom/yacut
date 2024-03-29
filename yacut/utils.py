import random

from yacut.constants_messages import CHARACTERS, SHORT_ID_LENGTH
from yacut.models import URLMap


def get_unique_short_id(length: int) -> str:
    """Формирование коротких идентификаторов переменной длины."""
    random_string = ''.join(random.choice(CHARACTERS) for _ in range(length))
    if check_short_id_in_db(random_string):
        return get_unique_short_id(SHORT_ID_LENGTH)
    return random_string


def check_short_id_in_db(short_id: str) -> bool:
    """Проверяет наличие заданного короткого идентификатора в БД."""
    return URLMap.query.filter_by(short=short_id).first() is not None
