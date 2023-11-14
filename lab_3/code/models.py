from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        # self.ID = uuid.uuid4().hex
        self.name = name

    def get_user(self):
        pass

    def del_user(self):
        pass


class Category(db.Model):
    __tablename__ = "categorys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name


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
