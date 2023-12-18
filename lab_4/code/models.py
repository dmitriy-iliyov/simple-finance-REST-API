from datetime import timedelta
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import func
from app import database
from flask_jwt_extended import *


class UserModel(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(20), unique=True, nullable=False)
    password = database.Column(database.String(20), unique=True, nullable=False)

    user_money = database.relationship("BankAccountModel", uselist=False, back_populates="user_account")
    record = database.relationship("RecordModel", back_populates="user", lazy="dynamic")

    def __init__(self, name, password):
        self.name = name
        self.password = pbkdf2_sha256.hash(password)

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        return create_access_token(identity=self.id, expires_delta=expire_delta)

    def authenticate(self, password):
        if not pbkdf2_sha256.verify(password, self.password):
            return False
        return True


class BankAccountModel(database.Model):
    __tablename__ = "accounts"

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey("users.id"), unique=True)
    money = database.Column(database.Float(precision=2), unique=False, nullable=False)

    user_account = database.relationship("UserModel", back_populates="user_money")

    def __init__(self, user_id, money):
        self.user_id = user_id
        self.money = money


class CategoryModel(database.Model):
    __tablename__ = "categories"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(20), unique=True, nullable=False)

    record = database.relationship("RecordModel", back_populates="category", lazy="dynamic")

    def __init__(self, name):
        self.name = name


class RecordModel(database.Model):
    __tablename__ = "records"

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey("users.id"), unique=False, nullable=False)
    category_id = database.Column(database.Integer, database.ForeignKey("categories.id"), unique=False, nullable=False)
    time = database.Column(database.TIMESTAMP, server_default=func.now())
    amount_of_expenditure = database.Column(database.Float(precision=2), unique=False, nullable=False)

    user = database.relationship("UserModel", back_populates="record")
    category = database.relationship("CategoryModel", back_populates="record")

    def __init__(self, user_id, category_id, amount_of_expenditure):
        self.user_id = user_id
        self.category_id = category_id
        self.amount_of_expenditure = amount_of_expenditure
