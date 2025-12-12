CREATE DATABASE IF NOT EXISTS localCopy;

CREATE TABLE IF NOT EXISTS UserData(
  Username varchar(255) NOT NULL,
  Password varchar(255) NOT NULL,
  UserID INTEGER NOT NULL PRIMARY KEY
);
  
CREATE TABLE IF NOT EXISTS gameData(
  UserID INTEGER NOT NULL FOREIGN KEY REFERENCES UserData(UserID),
  TimesPlayed varchar(255),
  Game varchar(255),
  TotalTime time(fsp),
  HighestPoint INTEGER
  HighestTime INTEGER
);