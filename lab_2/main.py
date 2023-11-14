import uuid

from flask import Flask, request, json

from models.category import Category
from models.record import Record
from models.user import User

app = Flask(__name__)

users = {}
categorys = {}
records = {}


@app.post('/user')
def create_user():
    user_data = request.get_json()
    user = User(**user_data)
    users[user.ID] = user
    return user.__dict__


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
    category = Category(**category_name)
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
    record = Record(userID, categoryID)
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
    app.run(debug=True)





