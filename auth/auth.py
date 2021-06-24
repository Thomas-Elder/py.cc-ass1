class Auth:

    loggedin = False
    user = None

    def __init__(self, datastore_client) -> None:
        pass

    def create(self):
        pass

    def login(self):
        self.loggedin = True

    def logout(self):
        self.loggedin = False