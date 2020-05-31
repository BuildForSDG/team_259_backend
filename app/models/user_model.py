from datetime import datetime

from marshmallow import Schema, fields

from . import db, ma

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # 0 is False
    # 1 is True
    # 2 is restored or False
    is_suspended = db.Column(db.Integer, default=0, nullable=False)

    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

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
    def fetch_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def fetch_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod  
    def update(cls, id, first_name=None, last_name=None, email=None, phone=None):
        record = cls.fetch_by_id(id)
        if first_name:
            record.first_name = first_name
        if last_name:
            record.last_name = last_name
        if email:
            record.email = email
        if phone:
            record.phone = phone
        db.session.commit()
        return True

    @classmethod
    def update_password(cls, id, password=None):
        record = cls.fetch_by_id(id)
        if password:
            record.password = password
        db.session.commit()
        return True

    @classmethod
    def suspend(cls, id, is_suspended=None):
        record = cls.fetch_by_id(id)
        if is_suspended:
            record.is_suspended = is_suspended
        db.session.commit()
        return True

    @classmethod
    def restore(cls, id, is_suspended=None):
        record = cls.fetch_by_id(id)
        if is_suspended:
            record.is_suspended = is_suspended
        db.session.commit()
        return True

    @classmethod
    def delete_by_id(cls, id):
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()
        return True

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'is_suspended', 'created', 'updated')
