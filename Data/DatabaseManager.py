#Methods to edit SQL database as callable python
#Do not call these functions (Test after cloud database is linked)

import sqlite3
sqliteConnection = sqlite3.connect('DatabaseLocalCopy.db')
cursor = sqliteConnection.cursor()

class DatabaseManager:
    
    def __init__(self):
        self.emptyIDs = []
        self.lastID = 0
        cursor.execute("""""") #create db

    def addUser(self, username, password):
        password = hash(password)
        if self.emptyIDs.length() == 0:
            userID = self.lastID
            self.lastID += 1
        else:
            userID = self.emptyIDs[0]
            self.emptyIDs.pop(0)
        cursor.execute(f"""INSTERT INTO UserData ({username}, {password}, {userID})""")

    def updateUsername(self, username, userID):
        cursor.execute(f"""UPDATE UserData SET Username = {username} WHERE UserId = {userID}""")

    def updateUserPassword(self, password, userID, hashtype): #Fix
        password = hash(password)
        cursor.execute(f"""UPDATE UserData SET Password = {password} WHERE UserId = {userID}""")

    def deleteUser(self, userID):
        cursor.execute(f"""DELETE FROM UserData WHERE UserId = {userID}""")
        self.emptyIDs.append[userID]

    def usernameExists (self, name): #Fix
        result = cursor.execute(f"""SELECT Username FROM UserData WHERE EXISTS(SELECT Username FROM UserData WHERE UserData.Username = {name})""")
        return result

    def checkPassword (self, password, userId): #Returns boolean if password is correct
        return (cursor.execute(f"""SELECT Password FROM UserData WHERE UserData.UserID = {userId}""") == hash(password))
    
    #Update game highest/endgame
    #each game leaderboard
        #Highest Point or Time highest to lowest and lowest to highest
        #Username
        #Top 10
        #User rank


#import subprocess
#subprocess.run(git pull)