from datetime import datetime
import re


class User:

    def __init__(self, name):
        self.ID = re.sub(r'\D', '', str(datetime.now()))
        self.name = name

    def __str__(self):
        return "{ userID : " + self.ID + "; userName : " + self.name + "; }"