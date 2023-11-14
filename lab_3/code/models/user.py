import os, sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        # self.ID = uuid.uuid4().hex
        self.name = name

    def get_user(self):
        pass

    def del_user(self):
        pass
