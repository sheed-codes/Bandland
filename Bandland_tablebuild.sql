DROP DATABASE IF EXISTS bandland;
CREATE DATABASE bandland;
USE bandland;

-- -------------------------
-- USER TABLE
-- -------------------------
CREATE TABLE UserAccount (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(80) UNIQUE NOT NULL,
    Bankroll DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

-- -------------------------
-- TEAM TABLE
-- -------------------------
CREATE TABLE Team (
    TeamID INT AUTO_INCREMENT PRIMARY KEY,
    TeamName VARCHAR(50) NOT NULL,
    League VARCHAR(10) NOT NULL
);

-- -------------------------
-- GAME TABLE
-- -------------------------
CREATE TABLE Game (
    GameID INT AUTO_INCREMENT PRIMARY KEY,
    HomeTeamID INT NOT NULL,
    AwayTeamID INT NOT NULL,
    GameDate DATE NOT NULL,
    HomeScore INT NOT NULL,
    AwayScore INT NOT NULL,
    League VARCHAR(10) NOT NULL,
    FOREIGN KEY (HomeTeamID) REFERENCES Team(TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES Team(TeamID)
);

-- -------------------------
-- BET TABLE
-- -------------------------
CREATE TABLE Bet (
    BetID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    GameID INT NOT NULL,
    BetType VARCHAR(30) NOT NULL,
    WagerAmount DECIMAL(10,2) NOT NULL,
    Pick VARCHAR(20),
    Result VARCHAR(20),
    Odds DECIMAL(5,2) NOT NULL,
    Payout DECIMAL(10,2),
    FOREIGN KEY (UserID) REFERENCES UserAccount(UserID),
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
);

-- -------------------------
-- TRANSACTION LOG
-- -------------------------
CREATE TABLE TransactionLog (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Type VARCHAR(50),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES UserAccount(UserID)
);

SELECT Username, Bankroll
FROM UserAccount;

SELECT Username, Bankroll
FROM UserAccount
ORDER BY Bankroll DESC
LIMIT 10;

SELECT Username, COUNT(*) AS TotalBets
FROM UserAccount u
JOIN Bet b ON u.UserID = b.UserID
GROUP BY Username;



