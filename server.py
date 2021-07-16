# THIS IS SERVER!

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from datetime import datetime
import time

from person import ProfileOfUsers
from person import ActiveUsers
from person import ChatRoomUsers

# cd pycharmprojects/server2

#    ngrok tcp 5050
#    taskkill /f /im ngrok.exe
#    netstat -a

# GLOBAL CONSTANTS

#HOST = "192.168.0.101"

HOST = 'localhost'
PORT = 5050

BUFSIZE = 512
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 50

# GLOBAL VARIABLES
myServer = socket(AF_INET, SOCK_STREAM)
myServer.bind(ADDR)


def broadcast(message):
    encodedMessage = message.encode("utf8")
    print(message)
    for i in ChatRoomUsers.AllChatRoomUsers.values():
        clientInfo = i.getClientInfo()
        clientInfo.send(bytes(encodedMessage))


def handleChatRoomCommunication(userProfile):
    clientInfo = userProfile.getClientInfo()
    username = userProfile.getUserName()
    displayName = userProfile.getDisplayName()
    message = displayName + " : " + "has joined the chat"
    broadcast(message)

    """ If user wants to change chat type"""
    backStatus = 0
    run = True
    while run:
        try:
            msg = clientInfo.recv(BUFSIZE).decode("utf8")  # continuously looking for messages from client
            message = displayName + " : " + msg
            if msg == ".quit":
                clientInfo.close()
                ChatRoomUsers.AllChatRoomUsers.pop(username)
                newmsg = displayName + " : " + "has left the chat"
                broadcast(newmsg)
                print(displayName + " : " + "left server")
                break

            elif msg == ".back":
                backStatus = 1
                ChatRoomUsers.AllChatRoomUsers.pop(username)

                backMessage = ".back"
                encodedBackMessage = backMessage.encode("utf8")
                clientInfo.send(bytes(encodedBackMessage))

                newmsg = displayName + " : " + "has left the chat"
                broadcast(newmsg)
                break

            else:
                broadcast(message)

        except Exception as e:
            print("[EXCEPTION OCCURRED] : Server unable to retrieve message from client")
            run = False

    if backStatus == 1:
        chatTypeSelection(userProfile)


def sendPersonalMessageToReceiver(userProfile, receivingContactUsername, message):
    time.sleep(0.5)
    # REACHED TILL HERE

    receivingContactUserProfile = None
    receivingContactClientInfo = None

    try:
        receivingContactUserProfile = ActiveUsers.AllActiveUsers.get(receivingContactUsername)
        receivingContactClientInfo = receivingContactUserProfile.getClientInfo()

    except Exception as e:
        print("[EXCEPTION OCCURRED] : Receiver does not exist.")
        return

    senderUsername = userProfile.getUserName()
    encodedSenderUsername = senderUsername.encode("utf8")
    encodedMessage = message.encode("utf8")

    receivingContactClientInfo.send(bytes(encodedSenderUsername))
    time.sleep(1)
    receivingContactClientInfo.send(bytes(encodedMessage))


def handlePersonalCommunication(userProfile):
    clientInfo = userProfile.getClientInfo()

    """ If user wants to change chat type then backStatus variable will be used."""
    backStatus = 0
    run = True
    while run:
        try:
            receivingContactUsername = clientInfo.recv(BUFSIZE).decode("utf8")

            if receivingContactUsername == ".quit":
                clientInfo.close()
                ActiveUsers.AllActiveUsers.pop(userProfile.getUserName())
                print(userProfile.getUserName() + " : " + "left server")
                break

            elif receivingContactUsername == ".back":
                backStatus = 1
                ActiveUsers.AllActiveUsers.pop(userProfile.getUserName())

                backMessage = ".back"
                encodedBackMessage = backMessage.encode("utf8")
                clientInfo.send(bytes(encodedBackMessage))
                break

            else:
                """ If client send quit request then below might create error 
                    so it is placed in else statement"""
                message = clientInfo.recv(BUFSIZE).decode("utf8")

                message = userProfile.getDisplayName() + " : " + message
                sendPersonalMessageToReceiver(userProfile, receivingContactUsername, message)

        except Exception as e:
            print("[EXCEPTION OCCURRED] : Server unable to retrieve message from client")
            run = False

    if backStatus == 1:
        chatTypeSelection(userProfile)


def chatTypeSelection(userProfile):
    clientInfo = userProfile.getClientInfo()
    userACTION = clientInfo.recv(BUFSIZE).decode("utf8")

    if userACTION == "CREATE_CHATROOM":
        pass

    elif userACTION == "JOIN_CHATROOM":
        ChatRoomUsers.AllChatRoomUsers[userProfile.getUserName()] = userProfile
        handleChatRoomCommunication(userProfile)

    elif userACTION == "PERSONAL_CHAT":
        ActiveUsers.AllActiveUsers[userProfile.getUserName()] = userProfile
        handlePersonalCommunication(userProfile)

    elif userACTION == ".quit":
        clientInfo.close()
        print(userProfile.getUserName() + " : " + "left server")


def getUserInfo(userProfile):
    clientInfo = userProfile.getClientInfo()

    username = clientInfo.recv(BUFSIZE).decode("utf8")  # receives a unique name from client.
    displayName = clientInfo.recv(BUFSIZE).decode("utf8")  # receives a display name from client.
    password = clientInfo.recv(BUFSIZE).decode("utf8")  # receives password from client.

    print("[NEW CONNECTION INFO]", end=" : ")
    print(username, displayName, password)

    userProfile.setUserName(username)
    userProfile.setDisplayName(displayName)
    userProfile.setPassword(password)

    chatTypeSelection(userProfile)


def wait_for_connections(myServer):
    print("0")
    run = True
    while run:
        try:
            print("1")
            clientInfo, clientAddress = myServer.accept()
            userProfile = ProfileOfUsers(clientInfo, clientAddress)
            print("2")

            t = time.localtime()
            currentTime = time.strftime("%H:%M:%S", t)
            print(f"[CONNECTION] : {clientAddress} connected to the server at {currentTime}")

            communicationThread = Thread(target=getUserInfo, args=(userProfile,))
            communicationThread.start()

        except Exception as e:
            print("[EXCEPTION] : ", e)
            run = False

    print("Server is currently unavailable")


if __name__ == "__main__":
    myServer.listen(MAX_CONNECTIONS)
    print("\nServer started successfully\n")
    wait_for_connections(myServer)
