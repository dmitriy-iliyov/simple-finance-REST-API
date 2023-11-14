import random
from datetime import datetime
import os, sys

sys.path.append(os.path.join(os.getcwd(), '..'))
from app import db


class Record(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(20), unique=True)
    categoryID = db.Column(db.String(20), unique=True)
    time = db.Column(db.String(20), unique=True)
    amountOfExpenditure = db.Column(db.String(20), unique=True)

    def __init__(self, userID, categoryID):
        self.userID = userID
        self.categoryID = categoryID
        self.time = str(datetime.now())
        self.amountOfExpenditure = str(random.randint(1, 100)) + "$"
