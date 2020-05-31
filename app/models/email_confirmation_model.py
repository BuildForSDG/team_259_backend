from datetime import datetime

from marshmallow import Schema, fields

from . import db, ma
from .user_model import User

class EmailConfirmation(db.Model):
    __tablename__='email_confirmations'
    id = db.Column(db.Integer, primary_key=True)
    email_is_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("sessions", single_parent=True, lazy=True))
    token = db.Column(db.String, unique=True, nullable=False)
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
    def update(cls, id, email_is_confirmed=None):
        record = cls.fetch_by_id(id)
        if email_is_confirmed:
            record.email_is_confirmed = email_is_confirmed
        db.session.commit()
        return True

    @classmethod
    def delete_by_id(cls, id):
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()
        return True

class EmailConfirmationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email_is_confirmed', 'user_id', 'token', 'created', 'updated')