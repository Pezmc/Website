from main import db
from markdown import markdown
from flask import Markup
from os import path

from .. import BaseModel


def role_name_to_markdown_file(role_name):
    res = role_name.lower().replace(" ", "-").replace("/", "-").replace(":", "")
    return "apps/volunteer/role_descriptions/" + res + ".md"


class Role(BaseModel):
    __tablename__ = "volunteer_role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    description = db.Column(db.String)
    # Things to know for the shift
    role_notes = db.Column(db.String)
    over_18_only = db.Column(db.Boolean, nullable=False, default=False)
    requires_training = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<VolunteerRole {0}>".format(self.name)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "role_notes": self.role_notes,
            "requires_training": self.requires_training,
        }

    def full_description(self):
        role_description_file = role_name_to_markdown_file(self.name)
        if not path.exists(role_description_file):
            return self.description

        content = open(role_description_file, "r").read()
        return Markup(markdown(content, extensions=["markdown.extensions.nl2br"]))

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(Role.name).all()


class RolePermission(BaseModel):
    __versioned__: dict = {}
    __tablename__ = "volunteer_role_permission"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)


"""
Qualifications include:
 - Over 18
 - Bar training
 - Bar supervisor training
 - DBS check (reduces min required for a shift)
 - Checked into site
 - Phone validated

class Qual(db.Model):
    __tablename__ = 'volunteer_qual'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)

class RoleQuals(db.Model):
    __tablename__ = 'volunteer_role_qual'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    qual_id = db.Column(db.Integer, db.ForeignKey('qual.id'), primary_key=True)
    required = db.Column(db.Boolean, nullable=False, default=False)
    self_certified = db.Column(db.Boolean, nullable=False, default=False)

class UserQuals(db.Model):
    __tablename__ = 'user_role_qual'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    qual_id = db.Column(db.Integer, db.ForeignKey('qual.id'), primary_key=True)
"""
