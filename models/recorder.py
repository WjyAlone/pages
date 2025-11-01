from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db

class Recorder(db.Model):
    __tablename__ = 'recorders'
    id = db.Column(db.Integer, primary_key=True)
    client_ip = db.Column(db.String(100), nullable=True)
    platform = db.Column(db.String(100), nullable=True)
    browser = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Recorder {self.name}>'
