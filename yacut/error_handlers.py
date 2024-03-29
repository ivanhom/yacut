from http import HTTPStatus
from typing import Union

from flask import jsonify, render_template
from flask.wrappers import Response
from werkzeug.exceptions import InternalServerError, NotFound

from yacut import app, db


class InvalidAPIUsage(Exception):
    """Кастомный класс исключения."""
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(
            self, message: str, status_code: Union[int, None] = None
    ) -> None:
        """Конструктор класса InvalidAPIUsage принимает на вход текст
        сообщения и статус-код ошибки (необязательно).
        """
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict[str, str]:
        """Метод для сериализации переданного сообщения об ошибке."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage) -> tuple[Response, int]:
    """Вывод сообщения об ошибке при неправильных запросах в API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error: NotFound) -> tuple[str, int]:
    """Вывод кастомного шаблона ошибки при статусе 404."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error: InternalServerError) -> tuple[str, int]:
    """Вывод кастомного шаблона ошибки при статусе 500 с откатом сессии БД."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
