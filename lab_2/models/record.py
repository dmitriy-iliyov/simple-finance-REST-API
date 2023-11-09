from datetime import datetime
import re


class Record:

    def __init__(self, userID, categoryID):
        self.ID = re.sub(r'\D', '', str(datetime.now()))
        self.userID = userID
        self.categoryID = categoryID
        self.time = datetime.now()
        self.amountOfExpenditure = 0

    def __str__(self):
        return "{ record : " + self.ID + "; userID : " + self.userID + "; categoryID : " + self.categoryID + "; time : " + self.time +"; amount : " + self.amountOfExpenditure + "; }"