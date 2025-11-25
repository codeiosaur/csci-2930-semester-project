--Do Not ReRun
CREATE DATABASE localCopy;

CREATE TABLE userData(
  Username varchar(255),
  Password varchar(255), --change to hash
  ID int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (ID)
);
  
CREATE TABLE gameData(
  UserID int,
  TimesPlayed varchar(255),
  Game varchar(255),
  TotalTime time(fsp),
  Highest int,
  PRIMARY KEY (ID)
);
