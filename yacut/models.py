from datetime import datetime

from flask import url_for

from yacut import db


class URLMap(db.Model):
    """Модель ссылки."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_view', link=self.short, _external=True)
        )
