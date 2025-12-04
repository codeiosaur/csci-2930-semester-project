#Methods to edit SQL database as callable python
#Do not call these functions (Test after cloud database is linked)

import sqlite3
sqliteConnection = sqlite3.connect('DatabaseLocalCopy.db')
cursor = sqliteConnection.cursor()

class DatabaseManager:
    emptyIDs = []
    lastID = 0
    def AddUser(self, username, password, userId): #fix
        cursor.execute(f"""INSTERT INTO UserData ({username}, {password}, {userId})""")
    def UpdateUser(self, username, userId):
        cursor.execute(f"""UPDATE UserData SET Username = {username} WHERE UserId = {userId}""")
    def UpdateUser(self, password, userId):
        cursor.execute(f"""UPDATE UserData SET Password = {password} WHERE UserId = {userId}""")
    def DeleteUser(self, userId): #fix
        cursor.execute(f"""DELETE FROM UserData WHERE UserId = {userId}""")
