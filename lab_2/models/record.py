import random
import uuid
from datetime import datetime


class Record:

    def __init__(self, userID, categoryID):
        self.ID = uuid.uuid4().hex
        self.userID = userID
        self.categoryID = categoryID
        self.time = datetime.now()
        self.amountOfExpenditure = str(random.randint(1, 100)) + "$"

    def __str__(self):
        return "{ recordID :" + self.ID + "; userID :" + str(self.userID) + "; categoryID :" + str(self.categoryID) + \
            "; creation time :" + str(self.time) + "; amount of expenditure :" + str(self.amountOfExpenditure) + "; }"

