
from .models.post import Post
from .models.user import User

class DB:

    users = {}
    posts = []
    #
    #
    #
    def __init__(self, datastore_client) -> None:
        # add test creds
        self.users[1] = User(1, 'tom', '1234')
    #
    #
    #
    def getuser(self, id):

        return self.users[id]

    #
    #
    #
    def setuser(self, id, username, password):

        self.users[id] = User(id, username, password)

    #
    #
    #
    def updateuser(self, id, username, password):

        self.users[id].username = username
        self.users[id].password = password
    
    #
    #
    #
    def checkpassword(self, id, password) -> bool:

        if id in self.users:
            return self.users[id].password == password
        else:
            return False

    #
    #
    #
    def addpost(self, subject, message, user):
        self.posts.append(Post(subject, message, user))

    def getposts(self):
        return self.posts