from flask import Flask, request, render_template

from models.category import Category
from models.user import User

app = Flask(__name__)

users = {}
categorys = {}
records = {}


# @app.route('/user', methods=['POST', 'GET'])
# def create_user():
#     if request.method == 'POST':
#         user = User(request.form["user_name"])
#         users[user.ID] = user
#         print("+ " + user.ID)
#         return "You created the user :" + str(user)
#     else:
#         return render_template("login_user.html")


@app.post('/user')
def create_user():
    user = User(request.get_json())
    users[user.ID] = user
    print("+ " + user.ID)
    return "You created the user :" + str(user)


@app.get('/user/<userID>')
def get_user(userID):
    return users[userID].name


@app.delete('/user/<userID>')
def delete_user(userID):
    del users[userID]
    print("- " + userID)
    return "You delete the user :" + str(users[userID])


@app.get('/users')
def get_users():
    return str(users.keys())


# @app.route('/category', methods=['POST', 'GET'])
# def create_category():
#     if request.method == 'POST':
#         category = Category(request.form["category_name"])
#         categorys[category.ID] = category
#         print("+ " + category.ID)
#         return "You created the category :" + str(category)
#     else:
#         return render_template("login_category.html")


# @app.delete('/category')
# def endpoint():
#     pass
#
#
# @app.get('/category')
# def endpoint():
#     pass
#
#

@app.route('/record', methods=['POST', 'GET'])
def create_record():
    if request.method == 'POST':
        records
    else:
        return render_template("login_record.html")

#
# @app.delete('/record/<record_id>')
# def endpoint():
#     pass
#
#
# @app.get('/record/<record_id>')
# def endpoint():
#     pass


if __name__ == "__main__":
    app.run(debug=True)





