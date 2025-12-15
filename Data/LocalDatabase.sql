CREATE TABLE IF NOT EXISTS UserData(
  Username varchar(255) NOT NULL,
  Password varchar(255) NOT NULL,
  UserID INTEGER NOT NULL PRIMARY KEY
);
  
CREATE TABLE IF NOT EXISTS GameData(
  UserID INTEGER NOT NULL,
  TimesPlayed varchar(255),
  Game varchar(255),
  TotalTime varchar(225),
  HighestPoint INTEGER
  HighestTime INTEGER
  FOREIGN KEY UserID REFERENCES UserData(UserID)
);