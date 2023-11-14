import os, sys

sys.path.append(os.path.join(os.getcwd(), '..'))
from app import db


class Category(db.Model):
    __tablename__ = "categorys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name
