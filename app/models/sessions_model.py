from datetime import datetime

from marshmallow import Schema, fields

from . import db, ma
from user_model import User

class Session(db.Model):
    __tablename__='sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_ip_address = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("sessions", single_parent=True, lazy=True))
    token = db.Column(db.String, nullable=False)
    # session_id VARCHAR(255)
    # session_status VARCHAR(45)
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def insert_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def fetch_all(cls):
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def delete_by_id(cls, id):
        record = cls.fetch_by_id(id)
        record.delete()
        db.session.commit()
        return True

class SessionSchema(ma.ModelSchema):
    class Meta:
        model = Session