from datetime import datetime

from marshmallow import Schema, fields

from . import db, ma
from .user_model import User

class ChangePasswordToken(db.Model):
    __tablename__ = 'change_passwords'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("change_passwords", single_parent=True, lazy=True))
    email = db.Column(db.String(50), nullable=False)
    reset_code = db.Column(db.String(225), nullable=False)
    is_expired = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def insert_record(self):
        db.session.add(self)
        db.session.commit()
        return self


    @classmethod
    def fetch_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def fetch_by_reset_code(cls, reset_code):
        return cls.query.filter_by(reset_code=reset_code).first()

    @classmethod
    def fetch_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def fetch_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def expire_token(cls, id, is_expired=None):
        record = cls.fetch_by_id(id)
        if is_expired:
            record.is_expired = is_expired
        db.session.commit()
        return True

    @classmethod
    def expire_token_by_user(cls, user_id, is_expired=None):
        record = cls.fetch_by_user_id(user_id)
        if is_expired:
            record.is_expired = is_expired
        db.session.commit()
        return True


class ChangePasswordTokenSchema(ma.Schema):
    class Meta:
        fields = ('id','email','reset_token', 'is_expired','created')
