import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import *
from flask_sqlalchemy import SQLAlchemy
from marshmallow import *
import db_work as dbw
import marshmallows


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
app.json_sort_keys = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
database = SQLAlchemy(app)
jwt = JWTManager(app)
dbWorker = dbw.DatabaseWorker(database)
dbWorker.create_tables()


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
   return (jsonify({
       "message": "The token has expired.",
        "error": "token_expired"
   }), 401)


@jwt.invalid_token_loader
def invalid_token_callback(error):
   return (jsonify({
       "message": "Signature verification failed.",
       "error": "invalid_token"
   }), 401)


@jwt.unauthorized_loader
def missing_token_callback(error):
   return (jsonify({
       "description": "Request does not contain an access token.",
       "error": "authorization_required"
   }), 401)


@app.route('/')
def healthcheck():
    return str(datetime.now()).split('.')[0] + " service is live"


@app.post('/user')
def create_user():
    from models import UserModel, BankAccountModel
    user_data = request.get_json()
    try:
        marshmallows.UserSchema().load({"name": user_data["name"], "password": user_data["password"]})
        if database.session.query(UserModel).filter(UserModel.name == user_data["name"]).first() is None:
            user = UserModel(user_data["name"], user_data["password"])
            dbWorker.add_data(user)
            marshmallows.BankAccountSchema().load({"user_id": user.id, "money": user_data["money"]})
            account = BankAccountModel(user.id, user_data["money"])
            dbWorker.add_data(account)
            return jsonify({"id": user.id, "name": user.name, "money": account.money, "password": user_data["password"]})
        else:
            return "UserExist, 404"
    except ValidationError as error:
        return error.messages


@app.post('/login-user')
def login_user():
    from models import UserModel
    user_name = request.args.get('user-name')
    password = request.args.get('password')
    try:
        user = database.session.query(UserModel).filter(UserModel.name == user_name).first()
        if user.authenticate(password):
            token = user.get_token()
            return jsonify({"access token": token})
        return "Incorrect password."
    except AttributeError:
        return "AttributeError, 404"


@app.get('/user/account')
@jwt_required()
def get_account():
    from models import BankAccountModel
    user_id = get_jwt_identity()
    try:
        account = database.session.query(BankAccountModel).filter(BankAccountModel.user_id == user_id).first()
        return jsonify({"user_id": account.user_id, "money": account.money})
    except AttributeError:
        return "AttributeError, 404"


@app.get('/user')
@jwt_required()
def get_user():
    from models import UserModel
    user_id = get_jwt_identity()
    try:
        user = database.session.query(UserModel).filter(UserModel.id == user_id).first()
        return jsonify({"id": user.id, "name": user.name, "money": user.user_money.money})
    except AttributeError:
        return "AttributeError, 404"


@app.delete('/user')
@jwt_required()
def delete_user():
    from models import UserModel
    user_id = get_jwt_identity()
    try:
        user = database.session.query(UserModel).filter(UserModel.id == user_id).first()
        deleted_user = {"id": user.id, "name": user.name}
        dbWorker.delete_data(user)
        return jsonify(deleted_user)
    except AttributeError:
        return "AttributeError, 404"


@app.get('/users')
def get_users():
    from models import UserModel
    users = [{"id": user.id, "name": user.name, "money": user.user_money.money} for user in database.session.query(UserModel).all()]
    return jsonify(users)


@app.post('/category')
def create_category():
    from models import CategoryModel
    category_data = request.get_json()
    try:
        marshmallows.CategorySchema().load({"name": category_data["name"]})
        if database.session.query(CategoryModel).filter(CategoryModel.name == category_data["name"]).first() is None:
            category = CategoryModel(category_data["name"])
            dbWorker.add_data(category)
            return jsonify({"id": category.id, "name": category.name})
        else:
            return "CategoryExist, 404"
    except ValidationError as error:
        return error.messages


@app.get('/category')
def get_category():
    from models import CategoryModel
    category_id = request.args.get('categoryID')
    try:
        marshmallows.CategorySchema().load({"id": category_id, "name": "instance"})
        try:
            category = database.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            return jsonify({"id": category.id, "name": category.name})
        except AttributeError:
            return "AttributeError, 404"
    except ValidationError as error:
        return error.messages


@app.get('/categories')
def get_categories():
    from models import CategoryModel
    categories = [{"id": category.id, "name": category.name} for category in database.session.query(CategoryModel).all()]
    return jsonify(categories)


@app.delete('/category')
def delete_category():
    from models import CategoryModel
    category_id = request.args.get('categoryID')
    try:
        category = database.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        deleted_category = {"id": category.id, "name": category.name}
        dbWorker.delete_data(category)
        return jsonify(deleted_category)
    except AttributeError:
        return "AttributeError, 404"


@app.post('/record')
@jwt_required()
def create_record():
    import models
    user_id = get_jwt_identity()
    category_id = request.args.get('categoryID')
    amountOfExpenditure = request.args.get('amount')
    try:
        marshmallows.RecordSchema().load({"user_id": user_id, "category_id": category_id, "amount_of_expenditure": amountOfExpenditure})
        if database.session.get(models.UserModel, user_id) is not None and database.session.get(models.CategoryModel, category_id) is not None:
            account = database.session.query(models.BankAccountModel).filter(models.BankAccountModel.user_id == user_id).first()
            if account is not None and account.money - float(amountOfExpenditure) > 0:
                account.money = account.money - float(amountOfExpenditure)
                dbWorker.upd_data()
                record = models.RecordModel(user_id, category_id, amountOfExpenditure)
                dbWorker.add_data(record)
                return jsonify({"id": record.id, "user_id": record.user_id, "category_id": record.category_id,
                                "time": record.time, "amount_of_expenditure": record.amount_of_expenditure})
            else:
                return "user account isn't exist or insufficient funds"
        else:
            return "user or category isn't exist"
    except ValidationError as error:
        return error.messages


@app.get('/record')
@jwt_required()
def get_record():
    from models import RecordModel
    user_id = get_jwt_identity()
    category_id = request.args.get('categoryID')
    try:
        marshmallows.RecordSchema().load({"user_id": user_id, "category_id": category_id, "amount_of_expenditure": 1.0})
        try:
            record = database.session.query(RecordModel).filter(RecordModel.user_id == user_id,
                                                                RecordModel.category_id == category_id).first()
            return jsonify({"id": record.id, "user_id": record.user_id, "category_id": record.category_id,
                            "time": record.time, "amount_of_expenditure": record.amount_of_expenditure})
        except AttributeError:
            return "AttributeError, 404"
    except ValidationError as error:
        return error.messages


@app.delete('/record')
@jwt_required()
def delete_record():
    from models import RecordModel
    record_id = request.args.get('recordID')
    if record_id.isdigit():
        try:
            record = database.session.query(RecordModel).filter(RecordModel.id == record_id).first()
            deleted_record = {"id": record.id, "user_id": record.user_id, "category_id": record.category_id,
                              "time": record.time, "amount_of_expenditure": record.amount_of_expenditure}
            dbWorker.delete_data(record)
            return jsonify(deleted_record)
        except AttributeError:
            return "AttributeError, 404"
    else:
        return "sqlalchemy.exc.DataError"


if __name__ == "__main__":
    app.run(debug=True)
