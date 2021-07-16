import os

class Variables:
    receiverUsername = None  # person to whom client is sending message.
    selectedContact = None  # contact selected by user in personal messages frame.

    #translationLanguage = 'en'
    personalTranslationLanguage = 'en'
    chatroomTranslationLanguage = 'en'

    personalMessageListbox = None  # Listbox
    contactListbox = None  # Listbox
    ChatRoomListbox = None  # Listbox
    END = None

    def __init__(self):
        pass

    @staticmethod
    def addContactToOfflineFile(contact):
        contactFileName = "contactList"
        path = os.path.abspath("")
        path = path + "\SysFiles\\" + contactFileName + ".txt"

        file = open(path, 'a')
        file.write(contact + "\n")
        file.close()

    @staticmethod
    def loadContactList():
        contactList = []

        contactFileName = "contactList"
        path = os.path.abspath("")
        path = path + "\SysFiles\\" + contactFileName + ".txt"

        try:
            file1 = open(path, 'r')
            messages = file1.readlines()
            for message in messages:
                contactList.append(message.strip())

        except Exception as e:
            pass

        contactListboxTEMP = Variables.contactListbox
        contactListboxTEMP.delete(0, Variables.END)

        for i in contactList:
            contactListboxTEMP.insert(Variables.END, i)

        """This contactList is used in checking if sender exist in user's contact list."""
        return contactList

    @staticmethod
    def checkIfSenderExistsInContactList(senderUsername):
        contactList = Variables.loadContactList()
        if senderUsername in contactList:
            return 1
        else:
            return 0


class CreateNecessaryDirectories:

    def __init__(self):
        pass

    @staticmethod
    def createContactsDirectory():
        try:
            dir1 = "SysFiles"
            dirPath1 = os.path.abspath("")
            path1 = os.path.join(dirPath1, dir1)
            os.mkdir(path1)
            dir2 = "Contacts"
            dirPath2 = os.path.abspath("") + "\\" + dir1
            path2 = os.path.join(dirPath2, dir2)
            os.mkdir(path2)

        except Exception as e:
            pass
            # print("Already created")
