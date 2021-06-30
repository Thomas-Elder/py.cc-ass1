
import io
from google.cloud import datastore
from google.cloud import storage

from PIL import Image
from datetime import datetime

from .models.post import Post
from .models.user import User

from .initialusers import initialusers

class DB:

    #
    #
    #
    def __init__(self):

        self.dataclient = datastore.Client()
        self.storeclient = storage.Client()
        #initialusers(self.dataclient, self.storeclient)

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
    # SET USER
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
        self.setavatar(id, image)

    #
    # SET PASSWORD
    #
    def setpassword(self, id, newpassword) -> None:
        """ Sets the password of the user with id, to new password

        Gets the user from datastore with this id, and update it's 
        password to newpassword.

        Parameters
        ----------
        id : str
        newpassword : str

        Returns
        -------
            None
        """

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
    # GET IMG
    #
    def getimg(self, id) -> str:
        """ Gets the public url of an image in Google Cloud Storage

        Gets the public url of the image stored in a Google Cloud Storage
        blob with this id.

        Parameters
        ----------
        id : str

        Returns
        -------
            str : the public url of the image
        """

        self.bucket = storage.Client().get_bucket('cc-ass1-317800.appspot.com')
        blob = self.bucket.blob(id)

        return blob.public_url

    #
    # SET AVATAR
    #
    def setavatar(self, id, image):
        """ Sends a resized image to Google Cloud Storage

        Takes the given image and resizes it to 120*120 before
        storing it in Google Cloud Storage, creating a blob with 
        the id passed.

        Parameters
        ----------
        id : str
        image : FileStorage object

        Returns
        -------
            None
        """

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
    # SET IMAGE
    #
    def setimg(self, id, image) -> None:
        """ Sends an image to Google Cloud Storage

        Takes the given image and stores it in Google Cloud Storage,
        creating a blob with the id passed. 

        Parameters
        ----------
        id : str
        image : FileStorage object

        Returns
        -------
            None
        """

        # Get project bucket, and create/access blob for this id
        self.bucket = storage.Client().get_bucket('cc-ass1-317800.appspot.com')
        blob = self.bucket.blob(id)

        # Resize image
        imagetosave = Image.open(image)
        #imagetosave.thumbnail((120, 120)) # resize img to avatar size
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
    # ADD POST
    #
    def addpost(self, subject, message, user, image) -> None:
        """ Adds post information to datastore and gcs

        Takes the subject, message, user and image params passed, and 
        creates a new datastore record in the posts kind, and adds a new 
        blob to gcs to store the image.

        It creates an id based on the current date and time, which is how 
        posts are selected on get. It also passes the user.id to datastore
        so that we can get the user for this post.

        Parameters
        ----------
        subject : str
        message : str
        user : User object
        image : FileStorage object

        Returns
        -------
            None
        """

        #
        date = datetime.now()
        id = date.strftime('%d%m%Y%H%M%S%f')

        #
        key = self.dataclient.key('posts', id)
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
    # UPDATE POST
    #
    def updatepost(self, id, subject, message, user, image) -> None:
        """ Updates a post

        Takes the subject, message, user and image params passed, and updates
        the post with key.id equal to the id passed in.

        Parameters
        ----------
        id : str
        subject : str
        message : str
        user : User
        image : FileStorage object

        Returns
        -------
            None
        """

        # remove existing post with id
        key = self.dataclient.key('posts', id)
        old = self.dataclient.get(key)
        self.dataclient.delete(old.key)
        
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
    # GET POSTS
    #
    def getposts(self, id=None) -> list:
        """ Returns a list of up to 10 posts.

        Returns a list of up to 10 posts for the given id, or a list of up to
        10 posts from all users if not given.

        Parameters
        ----------
        id : str, optional

        Returns
        -------
            a list of Post class objects
        """

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

        result.sort(key=lambda r: r.datetime, reverse=True)

        return result