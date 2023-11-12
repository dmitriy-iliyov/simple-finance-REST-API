import random
import uuid
from datetime import datetime


class Record:

    def __init__(self, userID, categoryID):
        self.ID = uuid.uuid4().hex
        self.userID = userID
        self.categoryID = categoryID
        self.time = str(datetime.now())
        self.amountOfExpenditure = str(random.randint(1, 100)) + "$"
