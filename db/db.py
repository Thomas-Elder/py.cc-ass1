
import io
import os
from google.cloud import datastore
from google.cloud import storage

from PIL import Image
from datetime import datetime

from .models.post import Post
from .models.user import User

class DB:

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
    def setuser(self, id, username, password, image):

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
        self.setimg(id, image)

    #
    #
    #
    def setpassword(self, id, newpassword):
        key = self.dataclient.key('users', id)
        user = self.dataclient.get(key)

        username = user['username']

        user.update(
            {
                'id': id,
                'username': username,
                'password': newpassword
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
    def setimg(self, id, image):

        # Get project bucket, and create/access blob for this id
        self.bucket = storage.Client().get_bucket('cc-ass1-317800.appspot.com')
        blob = self.bucket.blob(id)

        # Resize image
        imagetosave = Image.open(image)
        imagetosave.thumbnail((120, 120)) # resize img to avatar size
        imagetosave = imagetosave.convert('RGB') # convert to RGB

        # Convert to byte array for upload to gcs
        img_byte_arr = io.BytesIO() 
        imagetosave.save(img_byte_arr, format='JPEG') 
        img_byte_arr = img_byte_arr.getvalue()

        # Set blob.cache_control = 'public, max-age=0' as GC storage caches an image for an hour by default, 
        # but you want the user to see the changed avatar immediately.
        blob.cache_control = 'public, max-age=0' 

        # Upload.
        blob.upload_from_string(img_byte_arr, content_type='image/jpeg')


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

        #
        date = datetime.now()
        id = date.strftime('%d%m%Y%H%M%S%f')

        #
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

        #
        self.setimg(id, image)
        self.dataclient.put(post)

    #
    #
    #
    def updatepost(self, id, subject, message, user, image):

        # remove existing post with id
        key = self.dataclient.key('posts', id)
        old = self.dataclient.get(key)
        old.key.delete()
        
        # create new id and post
        date = datetime.now()
        id = date.strftime('%d%m%Y%H%M%S%f')

        #
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

        #
        self.setimg(id, image)
        self.dataclient.put(post)

    #
    #
    #
    def getposts(self, id=None):
        result = []

        if id == None:
            query = self.dataclient.query(kind='posts')
            posts = query.fetch(limit=10)
            self.bucket = storage.Client().get_bucket('cc-ass1-317800.appspot.com')

            for post in posts:
                blob = self.bucket.blob(post['id'])

                result.append(Post(
                    post['subject'],
                    post['message'],
                    self.getuser(post['user']),
                    blob.public_url,
                    id=post['id'],
                    datetime=post['datetime']
                ))

        else:

            query = self.dataclient.query(kind='posts')
            query.add_filter('user', '=', id)
            posts = query.fetch(limit=10)

            self.bucket = storage.Client().get_bucket('cc-ass1-317800.appspot.com')
            blob = self.bucket.blob(id)

            for post in posts:
                blob = self.bucket.blob(post['id'])

                result.append(Post(
                    post['subject'],
                    post['message'],
                    self.getuser(post['user']),
                    blob.public_url,
                    id=post['id'],
                    datetime=post['datetime']
                ))

        return result