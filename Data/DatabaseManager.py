#Methods to edit SQL database as callable python
#Do not call these functions (Test after cloud database is linked)

import sqlite3
sqliteConnection = sqlite3.connect('DatabaseLocalCopy.db')
cursor = sqliteConnection.cursor()

class DatabaseManager:
    
    def __init__(self):
        self.emptyIDs = []
        self.lastID = 0

    def AddUser(self, username, password):
        password = hash(password)
        if self.emptyIDs.length() == 0:
            userID = self.lastID
            self.lastID += 1
        else:
            userID = self.emptyIDs[0]
            self.emptyIDs.pop(0)
        cursor.execute(f"""INSTERT INTO UserData ({username}, {password}, {userID})""")

    def UpdateUser(self, username, userID):
        cursor.execute(f"""UPDATE UserData SET Username = {username} WHERE UserId = {userID}""")

    def UpdateUser(self, password, userID, hashtype): #Fix
        hash = cursor.execute(f"""HASHBYTES""")
        cursor.execute(f"""UPDATE UserData SET Password = {password} WHERE UserId = {userID}""")

    def DeleteUser(self, userID):
        cursor.execute(f"""DELETE FROM UserData WHERE UserId = {userID}""")
        self.emptyIDs.append[userID]

#import subprocess
#subprocess.run(git pull)