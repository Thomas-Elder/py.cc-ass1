from datetime import datetime

class Post():

    def __init__(self, subject, message, user, id=None, datetime=None):
        
        self.subject = subject
        self.message = message
        self.user = user
        self.datetime = datetime
        self.id = id

    def editmessage(self, message):
        self.message = message