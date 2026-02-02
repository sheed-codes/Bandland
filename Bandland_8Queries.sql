USE bandland;
SELECT COUNT(*) FROM UserAccount;
SELECT COUNT(*) FROM Team;
SELECT COUNT(*) FROM Game;
SELECT COUNT(*) FROM Bet;
SELECT COUNT(*) FROM TransactionLog;

SELECT Username, Bankroll
FROM UserAccount;
SELECT UserID, Bankroll
FROM UserAccount
ORDER BY Bankroll DESC
LIMIT 10;

SELECT UserID, Username, Bankroll
FROM UserAccount
ORDER BY UserID;

SELECT u.UserID, u.Username, COUNT(b.BetID) AS TotalBets
FROM UserAccount u
LEFT JOIN Bet b ON u.UserID = b.UserID
GROUP BY u.UserID, u.Username
ORDER BY TotalBets DESC;

SELECT u.UserID, u.Username, AVG(b.WagerAmount) AS AvgWager
FROM UserAccount u
LEFT JOIN Bet b ON u.UserID = b.UserID
GROUP BY u.UserID, u.Username
ORDER BY AvgWager DESC;

SELECT BetID, UserID, GameID, BetType, WagerAmount, Result, Payout
FROM Bet
ORDER BY BetID DESC
LIMIT 15;

SELECT 
    GameID,
    HomeTeamID,
    AwayTeamID,
    HomeScore,
    AwayScore,
    ABS(HomeScore - AwayScore) AS ScoreDiff
FROM Game
ORDER BY ScoreDiff ASC, GameID ASC
LIMIT 15;

SELECT 
    u.UserID,
    u.Username,
    SUM(b.Payout - b.WagerAmount) AS NetProfit
FROM UserAccount u
JOIN Bet b ON u.UserID = b.UserID
GROUP BY u.UserID, u.Username
ORDER BY NetProfit DESC;

SELECT 
    t.TeamName,
    SUM(CASE WHEN g.HomeTeamID = t.TeamID AND g.HomeScore > g.AwayScore THEN 1
             WHEN g.AwayTeamID = t.TeamID AND g.AwayScore > g.HomeScore THEN 1
             ELSE 0 END) AS Wins,
    SUM(CASE WHEN g.HomeTeamID = t.TeamID AND g.HomeScore < g.AwayScore THEN 1
             WHEN g.AwayTeamID = t.TeamID AND g.AwayScore < g.HomeScore THEN 1
             ELSE 0 END) AS Losses
FROM Team t
LEFT JOIN Game g 
    ON g.HomeTeamID = t.TeamID OR g.AwayTeamID = t.TeamID
GROUP BY t.TeamID, t.TeamName
ORDER BY Wins DESC, Losses ASC;
