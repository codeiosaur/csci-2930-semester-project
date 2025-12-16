import sqlite3

sqliteConnection = sqlite3.connect('LocalDatabase.db', isolation_level = None)
cursor = sqliteConnection.cursor()
sql = """CREATE TABLE IF NOT EXISTS UserData(
  Username TEXT NOT NULL,
  Password TEXT NOT NULL,
  UserID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
);
  
CREATE TABLE IF NOT EXISTS GameData(
  UserID INTEGER NOT NULL,
  TimesPlayed INTEGER,
  Game TEXT,
  TotalTime INTEGER,
  HighestPoint INTEGER,
  HighestTime INTEGER,
  FOREIGN KEY (UserID) REFERENCES UserData(UserID)
);"""
cursor.executescript(sql)

class DatabaseManager:
    def __init__(self):
        pass

    def addUser(self, username, password):
        password = hash(password)
        cursor.execute(f"""INSERT INTO UserData (Username, Password) VALUES (?, ?);""", (username, password,))

    def updateUsername(self, username, userID):
        cursor.execute(f"""UPDATE UserData SET Username = ? WHERE UserId = ?;""", (username, userID,))

    def updateUserPassword(self, password, userID):
        password = hash(password)
        cursor.execute(f"""UPDATE UserData SET Password = ? WHERE UserId = ?;""", (password, userID,))

    def deleteUser(self, userID):
        cursor.execute(f"""DELETE FROM UserData WHERE UserId = ?;""", (userID,))

    def usernameExists(self, name): #returns true if username exists in db, else returns false
        result = cursor.execute(f"""SELECT Username FROM UserData WHERE EXISTS(SELECT UserID FROM UserData WHERE UserData.Username = ?);""", (name,))
        return result.fetchone()

    def getUsername(self, userId):
        result = cursor.execute(f"""SELECT Username FROM UserData WHERE UserID = ?""", (userId))
        return result.fetchone()
    
    def getIdFromName(self, username): #returns userID
        result = cursor.execute(f"""SELECT UserID FROM UserData WHERE Username = ?;""", (username,))
        return result.fetchone()

    def checkPassword (self, password, userId): #Returns true if password is correct, else returns false
        result = cursor.execute(f"""SELECT Password FROM UserData WHERE UserData.UserID = ?;""", (userId) == hash(password))
        return result.fetchone()
    
    def endGame(self, point, score, userId, game, time): #Call this function at end of game to update stats
        first = cursor.execute(f"""SELECT UserID FROM GameData WHERE EXISTS UserID = ? AND Game = ?;""", (userId, game,)).fetchone()
        if point:
            timescore = None
        else:
            timescore = score
            score = None
        if first:
            if timescore == None:
                high = cursor.execute(f"""SELECT HighestPoint FROM GameData WHERE (UserID = ? AND Game = ?);""", (userId, game,)).fetchone()
                if score < high:
                    score = high
            else:
                high = cursor.execute(f"""SELECT HighestTime FROM GameData WHERE (UserID = ? AND Game = ?);""", (userId, game,)).fetchone()
                if timescore < high:
                    timescore = high
            time += cursor.execute(f"""SELECT TotalTime FROM GameData WHERE UserID = ? AND Game = ?;""", (userId, game,)).fetchone()
            played = cursor.execute(f"""SELECT TimesPlayed FROM GameData WHERE UserID = ? AND Game = ?;""", (userId, game,)).fetchone() + 1
            cursor.execute(f"""UPDATE GameData SET TimesPlayed = ?, TotalTime = ?, HighestPoint = ?, HighestTime = ? WHERE UserID = ? AND Game = ?;""", (played, time, score, timescore, userId, game,))
        else:
            cursor.execute(f"""INSERT INTO GameData (UserID, Game, TimesPlayed, Totaltime, HighestPoint, HighestTime) VALUES (?, 1, ?, ?, ?, ?);""", (userId, game, time, score, timescore,))

    def leaderboard(self, game, userId, point): #Returns a list containing a list of the highest 10 scores and the users score, a list of the corresponding usernames in order, and an integer for the user's rank
        if point:
            if len(cursor.execute(f"""SELECT *, HighestPoint FROM GameData WHERE Game = ?""").fetchall()) > 9:
                scores = cursor.execute(f"""SELECT HighestPoint FROM GameData WHERE Game = ? ORDER BY HighestPoint ASC LIMIT 10;""", (game,)).fetchall()
            else:
                scores = cursor.execute(f"""SELECT *, HighestPoint FROM GameData WHERE Game = ? ORDER BY HighestPoint ASC;""", (game,)).fetchall()
            score = cursor.execute(f"""SELECT HighestPoint FROM GameData WHERE UserID = ? and Game = ?;""", (userId, game,)).fetchone()
        else:
            if len(cursor.execute(f"""SELECT *, HighestTime FROM GameData WHERE Game = ? ORDER BY HighestTime DESC""", (game,)).fetchall()) > 9:
                scores = cursor.execute(f"""SELECT HighestTime FROM GameData WHERE Game = ? ORDER BY HighestTime DESC LIMIT 10;""", (game,)).fetchall()
            else:
                scores = cursor.execute(f"""SELECT *, HighestTime FROM GameData WHERE Game = ? ORDER BY HighestTime DESC;""", (game,)).fetchall()
            score = cursor.execute(f"""SELECT HighestTime FROM GameData WHERE UserID = ? and Game = ?;""", (userId, game,)).fetchone()
        usernames = cursor.execute(f"""SELECT UserID FROM GameData WHERE Game = ? ORDER BY HighestPoint ASC, HighestTime DESC LIMIT 10;""", (game,)).fetchall()
        for index in range(10):
            usernames[index] = cursor.execute(f"""SELECT Username FROM UserData WHERE UserID = ?;""", (usernames[index],)).fetchone()
        scores.append(score)
        usernames.append(cursor.execute(f"""SELECT Username FROM UserData WHERE UserID = ?;""", (userId,)).fetchone())
        rank = cursor.execute(f"""SELECT COUNT(*) FROM GameData WHERE Game = ? AND (HighestPoint !< ? OR HighestPoint = NULL) AND (HighestTime !> ? OR HighestTime = NULL);""", (game, score, score,)).fetchone()
        result = [scores, usernames, rank]
        return result
    
sqliteConnection.commit()