from datetime import datetime

class Post():

    def __init__(self, subject, message, user):
        #self.id = id
        self.subject = subject
        self.message = message
        self.user = user
        self.datetime = datetime.now()

    def editmessage(self, message):
        self.message = message