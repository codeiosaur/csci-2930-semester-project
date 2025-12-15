import sqlite3

sqliteConnection = sqlite3.connect('LocalDatabase.db', isolation_level = None)
cursor = sqliteConnection.cursor()
with open('C:\VS Code\csci-2930-semester-project\Data\LocalDatabase.sql', 'r') as file:
    sql_script = file.read()
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.executescript(sql_script)

emptyIDs = []
lastID = 0

class DatabaseManager:
    def __init__(self):
        pass

    def addUser(self, username, password):
        password = hash(password)
        if emptyIDs.length() == 0:
            userID = lastID
            lastID += 1
        else:
            userID = emptyIDs[0]
            emptyIDs.pop(0)
        cursor.execute(f"""INSTERT INTO UserData ({username}, {password}, {userID});""")

    def updateUsername(self, username, userID):
        cursor.execute(f"""UPDATE UserData SET Username = {username} WHERE UserId = {userID};""")

    def updateUserPassword(self, password, userID): #Fix
        password = hash(password)
        cursor.execute(f"""UPDATE UserData SET Password = {password} WHERE UserId = {userID};""")

    def deleteUser(self, userID):
        cursor.execute(f"""DELETE FROM UserData WHERE UserId = {userID};""")
        emptyIDs.append[userID]

    def usernameExists (self, name): #Fix
        result = cursor.execute(f"""SELECT Username FROM UserData WHERE EXISTS(SELECT Username FROM UserData WHERE UserData.Username = {name});""")
        return result

    def checkPassword (self, password, userId): #Returns boolean if password is correct
        return (cursor.execute(f"""SELECT Password FROM UserData WHERE UserData.UserID = {userId};""") == hash(password))
    
    def endGame(self, point, score, userId, game, time): #Call this function at end of game to update stats
        first = cursor.execute(f"""SELECT UserID FROM GameData WHERE EXISTS UserID = {userId} AND Game = {game};""")
        if point:
            timescore = None
        else:
            timescore = score
            score = None
        if first:
            if timescore == None:
                high = cursor.execute(f"""SELECT HighestPoint FROM GameData WHERE (UserID = {userId} AND Game = {game});""")
                if score < high:
                    high = score
            else:
                high = cursor.execute(f"""SELECT HighestTime FROM GameData WHERE (UserID = {userId} AND Game = {game});""")
                if timescore > high:
                    high = timescore
            time += cursor.execute(f"""SELECT TotalTime FROM GameData WHERE UserID = {userId} AND Game = {game};""")
            played = cursor.execute(f"""SELECT TimesPlayed FROM GameData WHERE UserID = {userId} AND Game = {game};""") + 1
            cursor.execute(f"""UPDATE GameData SET TimesPlayed = {played}, TotalTime = {time}, HighestPoint = {score}, HighestTime = {timescore} WHERE UserID = {userId} AND Game = {game};""")
        else:
            cursor.execute(f"""INSERT INTO GameData ({userId}, 1, {game}, {time}, {score}, {timescore});""")

    def leaderboard(self, game, userId, point): #Returns a list containing a list of the highest 10 scores and the users score, a list of the corresponding usernames in order, and an integer for the user's rank
        if point:
            scores = cursor.execute(f"""SELECT TOP 10 HighestPoint FROM GameData WHERE Game = {game} ORDER BY HighestPoint ASC;""")
            score = cursor.execute(f"""SELECT HighestPoint FROM GameData WHERE UserID = {userId} and Game = {game};""")
        else:
            scores = cursor.execute(f"""SELECT TOP 10 HighestTime FROM GameData WHERE Game = {game} ORDER BY HighestTime DESC;""")
            score = cursor.execute(f"""SELECT HighestTime FROM GameData WHERE UserID = {userId} and Game = {game};""")
        usernames = cursor.execute(f"""SELECT TOP 10 UserID FROM GameData WHERE Game = {game} ORDER BY HighestPoint ASC, HighestTime DESC;""")
        for index in range(10):
            usernames[index] = cursor.execute(f"""SELECT Username FROM UserData WHERE UserID = {usernames[index]};""")
        scores.append(score)
        usernames.append(cursor.execute(f"""SELECT Username FROM UserData WHERE UserID = {userId};"""))
        rank = cursor.execute(f"""SELECT COUNT(*) FROM GameData WHERE Game = {game} AND (HighestPoint !< {score} OR HighestPoint = NULL) AND (HighestTime !> {score} OR HighestTime = NULL);""")
        result = [scores, usernames, rank]
        return result
    
sqliteConnection.commit()
sqliteConnection.close()