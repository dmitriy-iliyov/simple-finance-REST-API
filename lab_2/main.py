from flask import Flask, request, jsonify

from models.category import Category
from models.record import Record
from models.user import User

app = Flask(__name__)

users = {}
categorys = {}
records = {}


@app.post('/user')
def create_user():
    user = User("sayner")
    users[user.ID] = user
    return "You created the user :" + str(user)


@app.get('/user/<userID>')
def get_user(userID):
    try:
        return str(users[userID])
    except KeyError:
       return "This user isn't exist."


@app.delete('/user/<userID>')
def delete_user(userID):
    try:
        result = "You delete the user :" + str(users[userID])
        del users[userID]
        return result
    except KeyError:
       return "This user isn't exist."


@app.get('/users')
def get_users():
    return str(users.keys())


@app.post('/category')
def create_category():
    category = Category("category_name")
    categorys[category.ID] = category
    print("+ " + category.ID)
    return "You created the category :" + str(category)


@app.get('/category/<categoryID>')
def get_category(categoryID):
    try:
        return str(categorys[categoryID])
    except KeyError:
       return "This category isn't exist."


@app.get('/categorys')
def get_categorys():
    return str(categorys.keys())


@app.delete('/category/<categoryID>')
def delete_category(categoryID):
    try:
        result = "You delete the user :" + str(categorys[categoryID])
        del categorys[categoryID]
        return result
    except KeyError:
       return "This category isn't exist."


@app.post('/record')
def create_record():
    userID = request.args.get('userID')
    categoryID = request.args.get('categoryID')
    record = Record(userID, categoryID)
    records[record.ID] = record
    return str(record)


@app.get('/record')
def get_record():
    userID = request.args.get('userID')
    categoryID = request.args.get('categoryID')
    try:
        for record in records.values():
            if record.userID == userID and record.categoryID == categoryID:
                return str(record)
            else:
                return "Record with this parametrs isn't exist."
    except KeyError:
       return "This category isn't exist."


@app.delete('/record/<recordID>')
def delete_record(recordID):
        try:
            result = "You delete the record :" + str(records[recordID])
            del records[recordID]
            return result
        except KeyError:
            return "This category isn't exist."


if __name__ == "__main__":
    app.run(debug=True)





