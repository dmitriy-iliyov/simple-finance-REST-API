from datetime import datetime
from app import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name


class CategoryModel(db.Model):
    __tablename__ = "categorys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name


class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(20), unique=True)
    categoryID = db.Column(db.String(20), unique=True)
    time = db.Column(db.String(20), unique=True)
    amountOfExpenditure = db.Column(db.String(20), unique=True)

    def __init__(self, userID, categoryID, amountOfExpenditure):
        self.userID = userID
        self.categoryID = categoryID
        self.time = str(datetime.now())
        self.amountOfExpenditure = amountOfExpenditure
