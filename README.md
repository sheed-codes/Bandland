# Bandland
a sportsbetting simulation database

# BANDLAND Sports Betting Database Project


## Project Overview
This project creates a sports-betting simulation database called **BANDLAND**. 
The goal is to design the schema, load sample data, and build an interactive Python program 
that runs SQL queries.

The database stores information about:
- Users  
- Teams  
- Games  
- Bets  
- Transactions  

After designing the relational schema and ER diagram, the database is populated with synthetic 
but realistic data:  
**105 users, 20 teams, 40 games, and 420+ bets.**

---

## Files Included
1. **bandland_schema.sql** – Creates all tables.
2. **seed_bets.py** – Populates the database with users, teams, games, and bets.
3. **run_queries.py** – Interactive terminal program that runs all queries.
4. **ER_Diagram.png** – Database ER diagram.
5. **README.md** – Project documentation.

---

## How to Set Up the Database

### 1. Create the database
```sql
CREATE DATABASE BANDLAND;
USE BANDLAND;

2. Apply the schema

Open bandland_schema.sql in MySQL Workbench → Run All.

3. Seed the data
cd ~/Desktop/CS315_FinalProject
python3 seed_bets.py

You should see:

Inserted 105 users  
Inserted 20 teams  
Inserted 40 games  
Inserted 420 bets  
DONE!

How to Run the Query Browser

python3 run_queries.py

You will see:

===== BANDLAND ANALYTICS MENU =====
1. List all users and bankrolls
2. Top 10 richest users
3. Total bets per user
4. Average wager amount
5. Last 15 bets
6. Closest games (score difference)
7. Total winnings/losses per user
8. Team win/loss frequencies
0. Exit


QUERIES (English + Relational Algebra)

Query 1 — List All Users and Bankrolls

English: Show each user’s gamertag and bankroll.
Relational Algebra: Π(UserID, Gamertag, Bankroll)(UserAccount)

Query 2 — Top 10 Highest Bankrolls

English: Rank users by bankroll and return the top 10.
Relational Algebra:τ↓10 ( τ_Bankroll↓ (UserAccount) )

Query 3 — Total Bets by Each User

English: Count how many bets each user placed.
Relational Algebra:Γ UserID, COUNT(BetID)->TotalBets (Bet)

Query 4 — Average Wager Amount Per User

English: Show the average wager amount per user.
Relational Algebra:Γ UserID, AVG(WagerAmount)->AvgWager (Bet)

Query 5 — Last 15 Bets Placed

English: Show the last 15 bets placed based on BetID.
Relational Algebra:τ↓15 (Bet)

Query 6 — Games With Closest Score Difference

English: Return games where the score difference is the smallest.
Relational Algebra:Compute |HomeScore - AwayScore|
τ ascending by difference

Query 7 — Total Winnings/Losses Per User

English: Sum payouts minus wagers to get net profit/loss per user.
Relational Algebra:Γ UserID, SUM(Payout - WagerAmount)->Net (Bet)

Query 8 — Team Win/Loss Frequency

English: Count how many games each team won and lost.
Relational Algebra:
Wins:Γ TeamID, COUNT(*)->Wins
(
  (σ(HomeScore>AwayScore) Π HomeTeamID→TeamID(Game))
  ∪
  (σ(AwayScore>HomeScore) Π AwayTeamID→TeamID(Game))
)
Γ TeamID, COUNT(*)->Losses
(
  (σ(HomeScore<AwayScore) Π HomeTeamID→TeamID(Game))
  ∪
  (σ(AwayScore<HomeScore) Π AwayTeamID→TeamID(Game))
)
Team ⟕ Wins ⟕ Losses

Query 0 — Exit

No relational algebra (interface logic only).



Tech Requirements

Python 3

mysql-connector-python

MySQL server (Workbench or CLI)

Install connector:pip install mysql-connector-python

pip install mysql-connector-python



Notes

Data is randomly generated but realistic based on actual sports structures.

This is a simulation only — not tied to real gambling.

All queries meet project Task 2 + Task 3 requirements.




LICENSE

MIT License

Copyright (c) 2025 sheed-codes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


END OF README

