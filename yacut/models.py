from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """Описание полей модели для записи в БД."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self) -> dict[str, str]:
        """Метод-сериализатор, используемый для
        преобразования объекта модели URLMap в словарь.
        """
        return dict(
            url=self.original,
            short_link=self.short
        )

    def from_dict(self, data: dict[str, str]) -> None:
        """Метод-десериализатор, используемый для
        добавления данных из словаря в объект модели URLMap.
        """
        fields = {'original': 'url', 'short': 'custom_id'}
        for field in fields.keys():
            request_fied = fields[field]
            if request_fied in data:
                setattr(self, field, data[request_fied])
