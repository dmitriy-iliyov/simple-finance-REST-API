import psycopg2
from collections import OrderedDict
from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import *
import marshmallows


def get_db_connection():
    # return psycopg2.connect(host="lab_3-db-1", database="database", user="admin", password="root")
    return psycopg2.connect(host="localhost", database="database", user="admin", password="root")


def create_tables():
    commands = (
        """ 
        CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR (20) NOT NULL);
        """,
        """ 
        CREATE TABLE categories ( 
                id SERIAL PRIMARY KEY, 
                name VARCHAR(20) NOT NULL 
                );
        """,
        """ 
        CREATE TABLE records ( 
                id SERIAL PRIMARY KEY,
                user_id INT,
                category_id INT, 
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                amount_of_expenditure FLOAT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
                );
        """)
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_data(data):
    db.session.add(data)
    db.session.commit()


def delete_data(data):
    db.session.delete(data)
    db.session.commit()


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
app.json.sort_keys = False
db = SQLAlchemy(app)
create_tables()


@app.post('/user')
def create_user():
    from models import UserModel
    user_data = request.get_json()
    try:
        marshmallows.UserSchema().load({"name": user_data["name"]})
        user = UserModel(user_data["name"])
        add_data(user)
        return jsonify({"id": user.id, "name": user.name})
    except ValidationError as error:
        print(error.messages)
        return error.messages


@app.get('/user')
def get_user():
    from models import UserModel
    user_id = request.args.get('userID')
    try:
        user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        return jsonify({"id": user.id, "name": user.name})
    except AttributeError:
        return 0


@app.delete('/user')
def delete_user():
    from models import UserModel
    user_id = request.args.get('userID')
    try:
        user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        deleted_user = {"id": user.id, "name": user.name}
        delete_data(user)
        return jsonify(deleted_user)
    except AttributeError:
        return 0


@app.get('/users')
def get_users():
    from models import UserModel
    users = [{"id": user.id, "name": user.name} for user in db.session.query(UserModel).all()]
    return jsonify(users)


@app.post('/category')
def create_category():
    from models import CategoryModel
    category_data = request.get_json()
    try:
        marshmallows.CategorySchema().load({"name": category_data["name"]})
        category = CategoryModel(category_data["name"])
        add_data(category)
        return jsonify({"id": category.id, "name": category.name})
    except ValidationError as error:
        print(error.messages)
        return error.messages


@app.get('/category')
def get_category():
    from models import CategoryModel
    category_id = request.args.get('categoryID')
    try:
        marshmallows.CategorySchema().load({"id": category_id, "name": "instance"})
        try:
            category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            return jsonify({"id": category.id, "name": category.name})
        except AttributeError:
            return 0
    except ValidationError as error:
        print(error.messages)
        return error.messages


@app.get('/categories')
def get_categories():
    from models import CategoryModel
    categories = [{"id": category.id, "name": category.name} for category in db.session.query(CategoryModel).all()]
    return jsonify(categories)


@app.delete('/category')
def delete_category():
    from models import CategoryModel
    category_id = request.args.get('categoryID')
    try:
        category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        deleted_category = {"id": category.id, "name": category.name}
        delete_data(category)
        return jsonify(deleted_category)
    except AttributeError:
        return 0


@app.post('/record')
def create_record():
    from models import RecordModel
    user_id = request.args.get('userID')
    category_id = request.args.get('categoryID')
    amountOfExpenditure = request.args.get('amount')
    try:
        marshmallows.RecordSchema().load({"user_id": user_id, "category_id": category_id, "amount_of_expenditure": amountOfExpenditure})
        record = RecordModel(user_id, category_id, amountOfExpenditure)
        add_data(record)
        return jsonify({"id": record.id, "user_id": record.user_id, "category_id": record.category_id,
                        "time": record.time, "amount_of_expenditure": record.amount_of_expenditure})
    except ValidationError as error:
        print(error.messages)
        return error.messages


@app.get('/record')
def get_record():
    from models import RecordModel
    user_id = request.args.get('userID')
    category_id = request.args.get('categoryID')
    try:
        marshmallows.RecordSchema().load({"user_id": user_id, "category_id": category_id, "amount_of_expenditure": 1.0})
        try:
            record = db.session.query(RecordModel).filter(RecordModel.user_id == user_id,
                                                          RecordModel.category_id == category_id).first()
            return jsonify({"id": record.id, "user_id": record.user_id, "category_id": record.category_id,
                            "time": record.time, "amount_of_expenditure": record.amount_of_expenditure})
        except AttributeError:
            return 0
    except ValidationError as error:
        print(error.messages)
        return error.messages


@app.delete('/record')
def delete_record():
    from models import RecordModel
    record_id = request.args.get('recordID')
    print(record_id)
    if isinstance(record_id, int):
        try:
            record = db.session.query(RecordModel).filter(RecordModel.id == record_id).first()
            deleted_record = {"id": record.id, "user_id": record.user_id, "category_id": record.category_id,
                              "time": record.time, "amount_of_expenditure": record.amount_of_expenditure}
            delete_data(record)
            return jsonify(deleted_record)
        except AttributeError:
            return 0
    else:
        return "sqlalchemy.exc.DataError"


if __name__ == "__main__":
    app.run(debug=True)
