import uuid


class User:

    def __init__(self, name):
        self.ID = uuid.uuid4().hex
        self.name = name

    def __str__(self):
        return "{ userID : " + self.ID + "; userName : " + self.name + "; }"