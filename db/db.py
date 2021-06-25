
from google.cloud import datastore

from datetime import datetime

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

        key = self.client.key('posts', '1')
        post = datastore.Entity(key=key)
        post.update(
            {
                'subject':'test post',
                'message':'test message',
                'user':'1',
                'datetime': datetime.now()
            }
        )

        self.client.put(post)

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
        pass

    #
    #
    #
    def updateuser(self, id, username, password):
        pass

    #
    #
    #
    def checkpassword(self, id, password) -> bool:

        key = self.client.key('users', id)
        result = self.client.get(key)

        if result != None and result['password'] == password:

            return User(result['id'], result['username'], result['password'])

        else:
            return False

    #
    #
    #
    def addpost(self, subject, message, user):

        key = self.client.key('posts')
        post = datastore.Entity(key=key)
        post.update(
            {
                'subject': subject,
                'message': message,
                'user': user.id,
                'datetime': datetime.now()
            }
        )

        self.client.put(post)      


    #
    #
    #
    def getposts(self):
        query = self.client.query(kind='posts')
        posts = query.fetch()

        return posts