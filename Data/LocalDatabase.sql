--Do Not Run
CREATE DATABASE IF NOT EXISTS localCopy;

CREATE TABLE IF NOT EXISTS UserData(
  Username varchar(255) NOT NULL,
  Password varchar(255) NOT NULL,
  ID int NOT NULL PRIMARY KEY
);
  
CREATE TABLE IF NOT EXISTS gameData(
  UserID int NOT NULL FOREIGN KEY REFERENCES UserData(ID),
  TimesPlayed varchar(255),
  Game varchar(255),
  TotalTime time(fsp),
  Highest int
);
