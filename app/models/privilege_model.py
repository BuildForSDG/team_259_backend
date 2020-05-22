from datetime import datetime

from marshmallow import Schema, fields

from . import db, ma

class Privilege(db.Model):
    __tablename__='priviliges'
    id = db.Column(db.Integer, primary_key=True)
    privilege = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

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
    def update(cls, id, privilege=None, description=None):
        record = cls.fetch_by_id(id)
        if privilege:
            record.privilege = privilege
        if description:
            record.description = description
        db.session.commit()
        return True

    @classmethod
    def delete_by_id(cls, id):
        record = cls.fetch_by_id(id)
        record.delete()
        db.session.commit()
        return True

class PrivilegeSchema(ma.ModelSchema):
    class Meta:
        model = Privilege