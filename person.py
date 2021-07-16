class ActiveUsers:
    """ Its a dictionary containing username and object of ProfileOfUsers class."""
    AllActiveUsers = {}

    def __init__(self):
        pass


class ChatRoomUsers:
    """ Its a dictionary containing username and object of {ProfileOfUsers} class of
        users who are in a chatroom"""
    AllChatRoomUsers = {}

    def __init__(self):
        pass


class ProfileOfUsers:

    def __init__(self, clientInfo, clientAddress):
        self.clientInfo = clientInfo
        self.clientAddress = clientAddress
        self.username = ""
        self.displayName = ""
        self.password = ""

    def getClientInfo(self):
        return self.clientInfo

    def getUserName(self):
        return self.username

    def getDisplayName(self):
        return self.displayName

    def setUserName(self, username):
        self.username = username

    def setDisplayName(self, displayName):
        self.displayName = displayName

    def setPassword(self, password):
        self.password = password
