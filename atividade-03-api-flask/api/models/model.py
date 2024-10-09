from api import mongo

class Routine():
    def __init__(self, title, task, date):
        self.title = title
        self.task = task
        self.date = date