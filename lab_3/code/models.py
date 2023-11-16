from datetime import datetime
from sqlalchemy import func
from app import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    record = db.relationship("RecordModel", back_populates="user", lazy="dynamic")

    def __init__(self, name):
        self.name = name


class CategoryModel(db.Model):
    __tablename__ = "categorys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic")

    def __init__(self, name):
        self.name = name


class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey("category.id"), unique=False, nullable=False)
    time = db.Column(db.TIMESTAMP, serve_default=func.now())
    amountOfExpenditure = db.Column(db.Float(precision=2), unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="record")
    category = db.relationship("CategoryModel", back_populates="record")

    def __init__(self, userID, categoryID, amountOfExpenditure):
        self.userID = userID
        self.categoryID = categoryID
        self.amountOfExpenditure = amountOfExpenditure
