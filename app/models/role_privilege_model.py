from datetime import datetime

from marshmallow import Schema, fields

from . import db, ma
from privilege_model import Privilege
from role_model import Role

class RolePrivilege(db.Model):
    __tablename__ = 'role_privileges'
    id = db.Column(db.Integer, primary_key=True)

    privilege_id = db.Column(db.Integer, db.ForeignKey('priviliges.id'), nullable=False)
    privilege = db.relationship('Privilege', backref=db.backref("role_privileges", single_parent=True, lazy=True))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref("role_privileges", single_parent=True, lazy=True))

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
    def update(cls, id, privilege_id=None, role_id=None):
        record = cls.fetch_by_id(id)
        if privilege_id:
            record.privilege_id = privilege_id
        if role_id:
            record.role_id = role_id
        db.session.commit()
        return True

    @classmethod
    def delete_by_id(cls, id):
        record = cls.fetch_by_id(id)
        record.delete()
        db.session.commit()
        return True

class RolePrivilegeSchema(ma.ModelSchema):
    class Meta:
        model = RolePrivilege
