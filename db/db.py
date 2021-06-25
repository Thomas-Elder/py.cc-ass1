
from google.cloud import datastore
from pyasn1.type.univ import Null

from .models.post import Post
from .models.user import User

class DB:

    users = {}
    posts = []
    #
    #
    #
    def __init__(self):

        self.client = datastore.Client()

        key = self.client.key('users', '1')
        user = datastore.Entity(key=key)
        user.update(
            {
                'id': '1', 
                'username':'tom', 
                'password':'1234'
            }
            )

        self.client.put(user)

    #
    #
    #
    def getusers(self):
        query = self.client.query(kind='users')
        users = query.fetch()

        return users

    #   
    #
    #
    def getuser(self, id):

        key = self.client.key('users', id)
        result = self.client.get(key)

        if result == None:
            return None

        else:
            user = User(result['id'], result['username'], result['password'])
            return user

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

        key = self.client.key('users', id)
        result = self.client.get(key)

        if result != Null and result['password'] == password:

            return User(result['id'], result['username'], result['password'])

        else:
            return False

    #
    #
    #
    def addpost(self, subject, message, user):
        self.posts.append(Post(subject, message, user))

    def getposts(self):
        return self.posts