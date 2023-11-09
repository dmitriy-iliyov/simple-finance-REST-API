from datetime import datetime
import re


class Category:

    def __init__(self, name):
        self.ID = re.sub(r'\D', '', str(datetime.now()))
        self.name = name

    def __str__(self):
        return "{ categoryID : " + self.ID + "; categoryName : " + self.name + "; }"