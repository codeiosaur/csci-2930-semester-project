--Do Not ReRun
CREATE DATABASE localCopy;

CREATE TABLE userData(
  Username varchar(255) NOT NULL,
  Password varchar(255) NOT NULL, --change to hash
  ID int NOT NULL PRIMARY KEY
);
  
CREATE TABLE gameData(
  UserID int NOT NULL FOREIGN KEY,
  TimesPlayed varchar(255),
  Game varchar(255),
  TotalTime time(fsp),
  Highest int
);
