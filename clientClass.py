from socket import AF_INET, socket, SOCK_STREAM
import time
import os

from variable import Variables
from handleTranslation import HandleTranslation

# GLOBAL CONSTANTS

#HOST = "192.168.0.101"

HOST = "localhost"
PORT = 5050

BUFSIZE = 512
FORMAT = "utf8"
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)


class Client:

    def __init__(self, top):
        self.top = top

    @staticmethod
    def addContactAutomatically(username):
        Variables.addContactToOfflineFile(username)
        Variables.loadContactList()

    @staticmethod
    def connectClientToServer():
        client_socket.connect(ADDR)

    def translateMessage(self, message, isChatRoom):

        if isChatRoom:
            translationLanguage = Variables.chatroomTranslationLanguage
        else:
            translationLanguage = Variables.personalTranslationLanguage

        translationObject = HandleTranslation(translationLanguage)
        translatedMessage = translationObject.translate(message)

        return translatedMessage

    def sendGivenMessage(self, message, isTranslation, isChatRoom=False):
        """ msg : message to be sent to server
            isTranslation : to determine if message is to be translated."""
        try:
            if isTranslation:
                message = self.translateMessage(message, isChatRoom)
            encodedMessage = message.encode(FORMAT)
            client_socket.send(encodedMessage)

            if message == ".quit":
                client_socket.close()
                self.top.quit()

        except Exception as e:
            print("[EXCEPTION] :  Error in sending message to server!")
            if message == ".quit":
                self.top.quit()

    def receiveChatRoomMessages(self):
        """ This function runs an infinte loop and look for messages from server side."""
        """ Sleep function is used to ensure that chatroom listbox variable is initialized"""
        time.sleep(1)
        run = True
        while run:
            try:
                message = client_socket.recv(BUFSIZE).decode()
                if message == ".back":
                    break

                Variables.ChatRoomListbox.insert(Variables.END, message)

            except Exception as e:
                print("Exception occurred in retrieving chat messages from server.", e)
                run = False

    def receivePersonalMessages(self):
        """ This function runs an infinite loop and look for messages from server side."""
        while True:
            try:
                senderUsername = client_socket.recv(BUFSIZE).decode()

                if senderUsername == ".back":
                    break

                message = client_socket.recv(BUFSIZE).decode()

                check = Variables.checkIfSenderExistsInContactList(senderUsername)

                if check == 0:
                    Client.addContactAutomatically(senderUsername)

                path = os.path.abspath("")
                path = path + "\SysFiles\Contacts\\" + senderUsername + ".txt"
                file = open(path, 'a')
                file.write(message + "\n")
                file.close()

                if senderUsername == Variables.selectedContact:
                    Variables.personalMessageListbox.insert(Variables.END, message)

            except Exception as e:
                print("Exception occurred in retrieving message from server.", e)
                break

    def sendLoginInfo(self, username, displayName, password):
        """ This function saves login info on client side and also send it to server.
            username : display name of client.
            password : password of client."""

        file = open("loginInfo.txt", 'w')
        file.write(username + "\n")
        file.write(displayName + "\n")
        file.write(password + "\n")
        file.close()

        Client.connectClientToServer()
        """ Wait for some time after connecting to server before sending any information."""
        time.sleep(2)

        self.sendGivenMessage(username, isTranslation=False)
        time.sleep(0.4)
        self.sendGivenMessage(displayName, isTranslation=False)
        time.sleep(0.4)
        self.sendGivenMessage(password, isTranslation=False)

    def checkLoginStatus(self):
        """ This function check if user if logged in or not.
            If already logged in, then directly starts app functionality
            else it opens login frame."""
        try:
            username = ""
            displayName = ""
            password = ""
            """ If this file doesn't exist, exceptions is raised and login form is opened"""
            file = open("loginInfo.txt", "r")

            login_info = file.readlines()
            count = 0
            for word in login_info:
                if count == 0:
                    username = word.strip()
                elif count == 1:
                    displayName = word.strip()
                elif count == 2:
                    password = word.strip()
                count += 1

            Client.connectClientToServer()
            """ Wait for some time after connecting to server before sending any information."""
            time.sleep(2)

            self.sendGivenMessage(username, isTranslation=False)
            time.sleep(0.4)
            self.sendGivenMessage(displayName, isTranslation=False)
            time.sleep(0.4)
            self.sendGivenMessage(password, isTranslation=False)
            return 2
            # raise_frame(f2)   # This might be used when more than 2 frames will be used.

        except Exception as e:
            return 1  # This means raise frame 1
