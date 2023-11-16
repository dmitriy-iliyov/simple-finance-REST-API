import psycopg2
from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import *
from sqlalchemy import create_engine

import marshmallows

app = Flask(__name__)
app.config.from_pyfile('database_config.py', silent=True)
db = SQLAlchemy(app)
# engine = create_engine(f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@localhost:5432/{os.environ["POSTGRES_DB"]}')


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="database",
        user="admin",
        password="root")
    return connection


def add_data(data):
    db.session.add(data)
    db.session.commit()


users = {}
categorys = {}
records = {}

cur = get_db_connection().cursor()
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
            'name varchar (20) NOT NULL);')


@app.post('/user')
def create_user():
    user_data = request.get_json()
    try:
        result = marshmallows.UserSchema().load({"name": user_data["name"]})
        return result
    except ValidationError as err:
        print(err.messages)
        return err.messages


@app.get('/user')
def get_user():
    try:
        userID = request.args.get('userID')
        return users[userID].__dict__
    except KeyError:
        return 0


@app.delete('/user')
def delete_user():
    try:
        userID = request.args.get('userID')
        result = users[userID]
        del users[userID]
        return result.__dict__
    except KeyError:
        return 0


@app.get('/users')
def get_users():
    return [user.__dict__
            for user in users.values()]


@app.post('/category')
def create_category():
    category_name = request.get_json()
    category = models.CategoryModel(**category_name)
    categorys[category.ID] = category
    return category.__dict__


@app.get('/category')
def get_category():
    try:
        categoryID = request.args.get('categoryID')
        return categorys[categoryID].__dict__
    except KeyError:
        return 0


@app.get('/categorys')
def get_categorys():
    return [category.__dict__
            for category in categorys.values()]


@app.delete('/category')
def delete_category():
    try:
        categoryID = request.args.get('categoryID')
        result = categorys[categoryID]
        del categorys[categoryID]
        return result.__dict__
    except KeyError:
        return 0


@app.post('/record')
def create_record():
    userID = request.args.get('userID')
    categoryID = request.args.get('categoryID')
    record = models.RecordModel(userID, categoryID)
    records[record.ID] = record
    return record.__dict__


@app.get('/record')
def get_record():
    userID = request.args.get('userID')
    categoryID = request.args.get('categoryID')
    try:
        for record in records.values():
            if record.userID == userID and record.categoryID == categoryID:
                return record.__dict__
            else:
                return "error"
    except KeyError:
        return 0


@app.delete('/record')
def delete_record():
    recordID = request.args.get('recordID')
    try:
        result = records[recordID]
        del records[recordID]
        return result.__dict__
    except KeyError:
        return 0


if __name__ == "__main__":
    import models

    app.run(debug=True)
