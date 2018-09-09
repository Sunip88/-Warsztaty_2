from controllers import clcrypto

class User(object):
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1

        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    #password_hash missing
    def set_password(self, password, salt):
        self.__hashed_password = clcrypto.password_hash(password, salt)