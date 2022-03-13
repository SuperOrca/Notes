from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024), nullable=False)

    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)

    def __repr__(self):
        return "<Item id={} note_id={}>".format(self.id, self.note_id)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    updated = db.Column(db.DateTime(), default=func.now(), onupdate=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    items = db.relationship("Item", backref="list", lazy=True)

    def __repr__(self):
        return "<Note id={} name={}>".format(self.id, self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created = db.Column(db.DateTime(), default=func.now())

    notes = db.relationship("Note", backref="list", lazy=True)

    def __repr__(self):
        return "<User id={} email={} username={}>".format(
            self.id, self.email, self.username
        )
