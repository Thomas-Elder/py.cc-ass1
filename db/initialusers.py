from PIL import Image
from google.cloud import datastore

def initialusers(dataclient, storeclient):
    ids = ['s33750870', 's33750871', 's33750872', 's33750873', 's33750874', 's33750875', 's33750876', 's33750877','s33750878','s33750879']
    imgs = ['img/0.jpg', 'img/1.jpg', 'img/2.jpg', 'img/3.jpg', 'img/4.jpg', 'img/5.jpg', 'img/6.jpg', 'img/7.jpg', 'img/8.jpg', 'img/9.jpg']
    names = ['Tom Elder0', 'Tom Elder1', 'Tom Elder2', 'Tom Elder3', 'Tom Elder4', 'Tom Elder5', 'Tom Elder6', 'Tom Elder7', 'Tom Elder8', 'Tom Elder9']
    passwords = ['012345', '123456', '234567', '345678', '456789', '567890', '678901', '789012', '890123', '901234']

    # images
    #bucket = storeclient.get_bucket('cc-ass1-317800.appspot.com')
    #for id, img in zip(ids, imgs):
    #    existing = Image.open(img)
    #    new = existing.resize((120, 120), Image.ANTIALIAS)
    #    new.save(img)

    #    blob = bucket.blob(id)
    #    blob.upload_from_filename(img)


    # users
    for id, name, password in zip(ids, names, passwords):
        key = dataclient.key('users', id)
        user = datastore.Entity(key=key)
        user.update(
            {
                'id': id, 
                'username': name, 
                'password': password
            }
            )
        
        dataclient.put(user)