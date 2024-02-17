drop table if exists User;
CREATE TABLE User (
  UserId TEXT,
  rating INTEGER,
  Location TEXT,
  Country TEXT,
  PRIMARY KEY (UserId)
);

drop table if exists Item;
CREATE TABLE Item (
  ItemId INTEGER,
  name TEXT,
  UserId TEXT,
  Currently REAL,
  First_Bid REAL,
  Number_of_Bids INTEGER,
  Started DATETIME,
  End DATETIME,
  Description TEXT,
  PRIMARY KEY (ItemId),
  FOREIGN KEY (UserId) REFERENCES User (UserId)
);

drop table if exists Bid;
CREATE TABLE Bid (
  ItemId INTEGER,
  UserId TEXT,
  BidTime DATETIME,
  Amount REAL,
  PRIMARY KEY (ItemId, UserId, BidTime),
  FOREIGN KEY (ItemId) REFERENCES Item (ItemId) FOREIGN KEY (UserId) REFERENCES User (UserId)
);

drop table if exists Category;
CREATE TABLE Category(
  ItemId INTEGER,
  Category_Name TEXT,
  PRIMARY KEY (ItemId, Category_Name),
  FOREIGN KEY (ItemId) REFERENCES Item (ItemId)
);