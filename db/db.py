
from google.cloud import datastore
from google.cloud import storage

from PIL import Image
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

        self.dataclient = datastore.Client()
        self.storeclient = storage.Client()

        # call initialusers (or maybe we call this soemthing else... )

    #
    #
    #
    def getusers(self):

        query = self.dataclient.query(kind='users')
        users = query.fetch()

        return users

    #   
    #
    #
    def getuser(self, id):

        key = self.dataclient.key('users', id)
        result = self.dataclient.get(key)

        if result == None:
            return None

        else:
            user = User(result['id'], result['username'], result['password'])
            return user
    
    #   
    #
    #
    def usernameexists(self, username):

        query = self.dataclient.query(kind="users")
        query.add_filter('username', '=', username)
        result = query.fetch()

        if result.num_results == 0:
            return False
        else:
            return True

    #   
    #
    #
    def idexists(self, id):

        key = self.dataclient.key('users', id)
        result = self.dataclient.get(key)

        if result == None:
            return False
        else:
            return True

    #
    #
    #
    def setuser(self, id, username, password, filename):

        key = self.dataclient.key('users', id)
        user = datastore.Entity(key=key)
        user.update(
            {
                'id': id, 
                'username': username, 
                'password': password
            }
            )

        self.dataclient.put(user)
        self.setimg(id, filename)

    #
    #
    #
    def getimg(self, id):
        self.bucket = storage.Client().get_bucket('cc-ass1-317800.appspot.com')
        blob = self.bucket.blob(id)

        return blob.public_url

    #
    #
    #
    def setimg(self, id, filename):
        self.bucket = storage.Client().get_bucket('cc-ass1-317800.appspot.com')
        blob = self.bucket.blob(id)

        existing = Image.open(filename)
        new = existing.resize((120, 120), Image.ANTIALIAS)
        new.save(filename)

        blob.upload_from_filename(filename)

    #
    #
    #
    def updateuser(self, id, username, password):
        pass

    #
    #
    #
    def checkpassword(self, id, password) -> bool:

        key = self.dataclient.key('users', id)
        result = self.dataclient.get(key)

        if result != None and result['password'] == password:

            return User(result['id'], result['username'], result['password'])

        else:
            return False

    #
    #
    #
    def addpost(self, subject, message, user, filename):

        date = datetime.now()
        id = date.strftime('%d%m%Y%H%M%S%f')

        key = self.dataclient.key('posts')
        post = datastore.Entity(key=key)
        post.update(
            {   
                'id': id,
                'subject': subject,
                'message': message,
                'user': user.id,
                'datetime': date
            }
        )

        self.setimg(id, filename)
        self.dataclient.put(post)      

    #
    #
    #
    def getposts(self, id=None):
        result = []

        if id == None:
            query = self.dataclient.query(kind='posts')
            posts = query.fetch(limit=10)

            for post in posts:
                result.append(Post(
                    post['subject'],
                    post['message'],
                    self.getuser(post['user']),
                    id=post['id'],
                    datetime=post['datetime']
                ))

        else:

            query = self.dataclient.query(kind='posts')
            query.add_filter('user', '=', id)
            posts = query.fetch(limit=10)

            for post in posts:
                result.append(Post(
                    post['subject'],
                    post['message'],
                    self.getuser(post['user']),
                    id=post['id'],
                    datetime=post['datetime']
                ))

        return result