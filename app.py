import os
import time
from tkinter import *
from tkinter import ttk
from threading import Thread
from googletrans import LANGUAGES

from clientClass import Client
from variable import Variables
from variable import CreateNecessaryDirectories

from PIL import ImageTk

top = Tk()
top.geometry("1199x600+100+50")
top.resizable(False, False)
top.title("Anuvad")

user = Client(top)


def on_closing(event=None):
    """ This function is called when the window is closed by using X button.
        An error occurs if client is not properly disconnected from server that's why
        this function is important."""
    msg = ".quit"
    user.sendGivenMessage(msg, isTranslation=False)


def raise_frame(givenFrame):
    givenFrame.tkraise()


loginFrame = Frame(top, bg="#dbc6bd")
chatChoiceFrame = Frame(top, bg="#dbc6bd")
chatRoomFrame = Frame(top, bg="#dbc6bd")
personalMessageFrame = Frame(top, bg="#dbc6bd")

Image = ImageTk.PhotoImage(file="bg1.jpg")
ImageLabel = Label(top, image=Image).place(x=0, y=0, relwidth=1, relheight=1)

for frame in (loginFrame, chatChoiceFrame, chatRoomFrame, personalMessageFrame):
    frame.grid(row=0, column=0, sticky='news')

# FRAME 1
loginFrame.place(x=50, y=35, height=535, width=1100)


def loginButton():
    username = usernameVariable.get()
    displayName = displayNameVariable.get()
    password = passwordVariable.get()
    user.sendLoginInfo(username, displayName, password)
    raise_frame(chatChoiceFrame)


title = Label(loginFrame, text="Anuvad", font=("Impact", 35, "bold"),
              fg="#b33c00", bg="#dbc6bd").place(x=90, y=30)
desc = Label(loginFrame, text="SIGNUP HERE", font=("Goudy old style", 15, "bold"),
             fg="#b33c00", bg="#dbc6bd").place(x=90, y=100)
"""username"""
usernameVariable = StringVar()
usernameLabel = Label(loginFrame, text="Enter your Username", font=("Goudy old style", 15, "bold"),
                      fg="grey", bg="#dbc6bd").place(x=90, y=140)
usernameTextField = Entry(loginFrame, font=("times new roman", 15), textvariable=usernameVariable, bg="lightgray")
usernameTextField.bind("<Return>", loginButton)
usernameTextField.place(x=90, y=170, width=350, height=35)
"""displayName"""
displayNameVariable = StringVar()
displayNameLabel = Label(loginFrame, text="Enter your Display Name", font=("Goudy old style", 15, "bold"),
                         fg="grey", bg="#dbc6bd").place(x=90, y=210)
displayNameTextField = Entry(loginFrame, font=("times new roman", 15), textvariable=displayNameVariable, bg="lightgray")
displayNameTextField.bind("<Return>", loginButton)
displayNameTextField.place(x=90, y=240, width=350, height=35)
"""password"""
passwordVariable = StringVar()
passwordLabel = Label(loginFrame, text="Create your Password", font=("Goudy old style", 15, "bold"),
                      fg="grey", bg="#dbc6bd").place(x=90, y=280)
passwordTextField = Entry(loginFrame, font=("times new roman", 15), textvariable=passwordVariable, bg="lightgray")
passwordTextField.bind("<Return>", loginButton)
passwordTextField.config(show="*")
passwordTextField.place(x=90, y=315, width=350, height=35)
"""login button"""
loginButton = Button(loginFrame, command=loginButton, text="Login", cursor="hand2",
                     fg="white", bg="#b33c00", font=("times new roman", 14)).place(x=290, y=355, width=150, height=30)

# FRAME 2
chatChoiceFrame.place(x=50, y=35, height=535, width=1100)


def startChatRoom():
    raise_frame(chatRoomFrame)
    user.sendGivenMessage("JOIN_CHATROOM", isTranslation=False)
    """ This thread starts an infinite loop that receives chat room messages."""
    receiveMessagesThread = Thread(target=user.receiveChatRoomMessages)
    receiveMessagesThread.start()


def startPersonalMessaging():
    raise_frame(personalMessageFrame)
    user.sendGivenMessage("PERSONAL_CHAT", isTranslation=False)
    """ This thread starts an infinite loop that receives personal messages."""
    receiveMessagesThread = Thread(target=user.receivePersonalMessages)
    receiveMessagesThread.start()


chatChoiceTitle = Label(chatChoiceFrame, text="Select your choice", font=("Impact", 35, "bold"),
                        fg="yellow", bg="green").place(x=320, y=70)

startChatRoomButton = Button(chatChoiceFrame, command=startChatRoom, text="Join Global Chatroom", cursor="hand2",
                             fg="white", bg="#b33c00", font=("times new roman", 16)).place(x=400, y=170, width=220,
                                                                                           height=70)

startPersonalMessagingButton = Button(chatChoiceFrame, command=startPersonalMessaging, text="Personal Messaging",
                                      cursor="hand2", fg="white", bg="#b33c00", font=("times new roman", 16)).place(
    x=400, y=270, width=220,
    height=70)

# FRAME 3
chatRoomFrame.place(x=50, y=35, height=535, width=1100)


def sendChatRoomMessageButton():

    chatRoomTranslationLang = chatRoomLang.get()
    Variables.chatroomTranslationLanguage = chatRoomTranslationLang

    message = chatRoomMessageVariable.get()
    chatRoomMessageVariable.set("")
    print("message sent")
    user.sendGivenMessage(message, isTranslation=True, isChatRoom=True)


def chatroomBackButton():
    user.sendGivenMessage(".back", isTranslation=False)
    raise_frame(chatChoiceFrame)
    Variables.ChatRoomListbox.delete(0, Variables.END)


""" Chat Room Listbox"""
sbar = Scrollbar(chatRoomFrame)
chatRoomListbox = Listbox(chatRoomFrame, font=("times new roman", 15), height=15, width=105, bg="#dbc6bd",
                          yscrollcommand=sbar.set)
sbar.pack(side=RIGHT, fill=Y)
chatRoomListbox.place(x=10, y=60)

""" Chatroom Combobox"""
language = list(LANGUAGES.values())
chatRoomLang = ttk.Combobox(chatRoomFrame, values=language, width=22)
chatRoomLang.place(x=790, y=20, width=200, height=30)
chatRoomLang.set("Select Language")


""" Chatroom Message Textfield and Button"""
chatRoomMessageVariable = StringVar()
chatRoomMessageVariable.set("")

chatTextField = Entry(chatRoomFrame, font=("times new roman", 15), bg="lightgray", textvariable=chatRoomMessageVariable)
chatTextField.bind("<Return>", sendChatRoomMessageButton)
chatTextField.place(x=10, y=450, width=850, height=40)
chatRoomSendButton = Button(chatRoomFrame, text="Send", command=sendChatRoomMessageButton, cursor="hand2",
                            fg="white", bg="#b33c00", font=("times new roman", 14))
chatRoomSendButton.place(x=900, y=450, width=150, height=40)

""" Back Button"""
chatBackButton = Button(chatRoomFrame, text="<- Back", command=chatroomBackButton, cursor="hand2",
                        fg="white", bg="#b33c00", font=("times new roman", 14))
chatBackButton.place(x=10, y=10, width=110, height=40)

# Add values in Variables class
Variables.ChatRoomListbox = chatRoomListbox

# Frame 4
personalMessageFrame.place(x=50, y=35, height=535, width=1100)


def loadSelectedContactMessages(selectedUsername):
    personalMessageListboxTEMP = Variables.personalMessageListbox
    personalMessageListboxTEMP.delete(0, Variables.END)
    END = Variables.END

    path = os.path.abspath("")
    path = path + "\SysFiles\Contacts\\" + selectedUsername + ".txt"

    try:
        file1 = open(path, 'r')
        messages = file1.readlines()
        for message in messages:
            personalMessageListboxTEMP.insert(END, message)

    except Exception as e:
        personalMessageListboxTEMP.delete(0, Variables.END)


def cursorSelectionInListbox(event):
    try:
        widget = event.widget
        selection = widget.curselection()
        selectedUsername = widget.get(selection[0])

        Variables.selectedContact = selectedUsername
        Variables.receiverUsername = selectedUsername

        loadSelectedContactMessages(selectedUsername)  # start a function that loads msg_list using file handling

    except Exception as e:
        pass


def sendPersonalMessageButton():

    personalTranslationLang = personalChatLang.get()
    Variables.personalTranslationLanguage = personalTranslationLang

    personalMessage = personalMessageVariable.get()
    personalMessageVariable.set("")

    receiverUsername = Variables.receiverUsername

    translatedPersonalMessage = user.translateMessage(personalMessage, isChatRoom=False)

    # write sender's own message to text files.
    path = os.path.abspath("")
    path = path + "\SysFiles\Contacts\\" + receiverUsername + ".txt"

    file = open(path, 'a')
    file.write("You : " + translatedPersonalMessage + "\n")
    file.close()

    # show sender's  message to personalMessageList.
    modifiedMessage = "You : " + translatedPersonalMessage
    Variables.personalMessageListbox.insert(Variables.END, modifiedMessage)

    user.sendGivenMessage(receiverUsername, isTranslation=False)
    time.sleep(0.4)
    user.sendGivenMessage(translatedPersonalMessage, isTranslation=False)


def addContactManually():
    contactToBeAdded = addContactVariable.get()
    addContactVariable.set("")
    Variables.addContactToOfflineFile(contactToBeAdded)
    Variables.loadContactList()


def personalMessagesBackButton():
    user.sendGivenMessage(".back", isTranslation=False)
    raise_frame(chatChoiceFrame)


""" Contacts Listbox """
contactListbox = Listbox(personalMessageFrame, height=16, width=20, font=("times new roman", 15), bg="#dbc6bd")
contactListbox.bind('<<ListboxSelect>>', cursorSelectionInListbox)
contactListbox.place(x=10, y=56)

""" Combobox"""
#language = list(LANGUAGES.values())
language = ['NONE', 'bosnian', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'finnish',
            'french', 'german', 'indonesian', 'irish', 'italian', 'latin', 'spanish', 'swedish']
personalChatLang = ttk.Combobox(personalMessageFrame, values=language, width=22)
personalChatLang.place(x=790, y=20, width=200, height=30)
personalChatLang.set("Select Language")


""" Personal Messages Listbox"""
personalMessageListScrollbar = Scrollbar(personalMessageFrame)
personalMessageListbox = Listbox(personalMessageFrame, height=16, width=80, font=("times new roman", 15), bg="#dbc6bd",
                                 yscrollcommand=personalMessageListScrollbar.set)
personalMessageListScrollbar.pack(side=RIGHT, fill=Y)
personalMessageListbox.place(x=240, y=56)

""" Message Textfield and Button"""
personalMessageVariable = StringVar()
personalMessageVariable.set("")

personalMessageTextField = Entry(personalMessageFrame, width=80, font=("times new roman", 15), bg="lightgray",
                                 textvariable=personalMessageVariable)
personalMessageTextField.bind("<Return>", sendPersonalMessageButton)
personalMessageTextField.place(x=240, y=445)
personalMessageSendButton = Button(personalMessageFrame, width=16, text="Send", command=sendPersonalMessageButton,
                                   cursor="hand2",
                                   fg="white", bg="#b33c00", font=("times new roman", 14))
personalMessageSendButton.place(x=480, y=488)

""" Add Contact Textfield and Button"""
addContactVariable = StringVar()
addContactVariable.set("")

addContactTextField = Entry(personalMessageFrame, width=20, font=("times new roman", 15), bg="lightgray",
                            textvariable=addContactVariable)
addContactTextField.bind("<Return>", addContactManually)
addContactTextField.place(x=10, y=445)
addContactButton = Button(personalMessageFrame, text="Add Contact", command=addContactManually, cursor="hand2",
                          fg="white", bg="#b33c00", font=("times new roman", 14))
addContactButton.place(x=45, y=488)

""" Back Button"""
personalBackButton = Button(personalMessageFrame, width=10, text="<- Back", command=personalMessagesBackButton,
                            cursor="hand2",
                            fg="white", bg="#b33c00", font=("times new roman", 14))
personalBackButton.place(x=10, y=10, width=110, height=40)

# Add values in Variables class
Variables.personalMessageListbox = personalMessageListbox
Variables.contactListbox = contactListbox
Variables.END = END

Variables.loadContactList()

""" __main__() """

CreateNecessaryDirectories.createContactsDirectory()

st = user.checkLoginStatus()
if st == 1:
    raise_frame(loginFrame)
else:
    raise_frame(chatChoiceFrame)


top.protocol("WM_DELETE_WINDOW", on_closing)
top.mainloop()

