
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
        self.bucket = self.storeclient.get_bucket('cc-ass1-317800.appspot.com')
        id = 's33750870'
        file = 'img/0.jpg'

        img = Image.open(file)
        img.resize((120, 120), Image.ANTIALIAS)
        img.save(file)

        blob = self.bucket.blob(id)
        blob.upload_from_filename(file)

        key = self.dataclient.key('users', 's33750870')
        user = datastore.Entity(key=key)
        user.update(
            {
                'id': 's33750870', 
                'username':'Tom Elder0', 
                'password':'012345'
            }
            )

        self.dataclient.put(user)

        key = self.dataclient.key('posts', '1')
        post = datastore.Entity(key=key)
        post.update(
            {
                'id':'1',
                'subject':'test post',
                'message':'test message',
                'user':'1',
                'datetime': datetime.now()
            }
        )

        self.dataclient.put(post)

    #
    # Clean! 
    #
    def clean(self):
        # ok we need to delete all posts 
        # remove all users
        # delete all blobs in the bucket
        pass

    #
    # Init
    #
    def init(self):
        # create 10 user accounts
        # upload images
        pass

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
        print(result)
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
    def setuser(self, id, username, password):

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
    def addpost(self, subject, message, user, image):

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

        #blob = self.bucket.blob(id)
        #blob.upload_from_filename(image)

        self.dataclient.put(post)      


    #
    #
    #
    def getposts(self):

        query = self.dataclient.query(kind='posts')
        posts = query.fetch(limit=10)

        result = []

        for post in posts:
            result.append(Post(
                post['subject'],
                post['message'],
                self.getuser(post['user']),
                id=post['id'],
                datetime=post['datetime']
            ))

        return result
