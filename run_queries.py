import mysql.connector

# ----------------------------------------------
# CONNECT TO BANDLAND DATABASE
# ----------------------------------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # update if needed
        database="bandland"
    )

# ----------------------------------------------
# QUERY FUNCTIONS
# ----------------------------------------------
def run_query(cursor, query, headers=None):
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        if headers:
            print("\n" + " | ".join(headers))
            print("-" * 60)

        for row in rows:
            print(" | ".join(str(col) for col in row))

        print()
    except Exception as e:
        print("\n[ERROR RUNNING QUERY]", e, "\n")


# ----------------------------------------------
# MENU LOOP
# ----------------------------------------------
def main():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n===============================================")
    print(" 🎰 WELCOME TO BANDLAND QUERY BROWSER 🎰")
    print(" A sports betting simulation database.")
    print("===============================================\n")

    while True:
        print("====== 🎲 BANDLAND ANALYTICS MENU 🎲 ======")
        print("Select a query to run:\n")
        print("1. List all users and their bankrolls")
        print("2. Top 10 users with the highest bankroll")
        print("3. Total bets placed by each user")
        print("4. Average wager amount per user")
        print("5. Show last 15 bets placed")
        print("6. Games with the closest score difference")
        print("7. Total winnings/losses for each user")
        print("8. Team win/loss frequency (based on games)")
        print("0. Exit\n")

        choice = input("Enter your choice: ").strip()

        # ------------------------------
        # OPTION 0: EXIT
        # ------------------------------
        if choice == "0":
            print("\nExiting BandLand Query Browser… Goodbye!\n")
            break

        # ------------------------------
        # OPTION 1
        # ------------------------------
        elif choice == "1":
            print("\nRunning Query 1: List all users and bankrolls")
            query = """
                SELECT Username, Bankroll
                FROM UserAccount
                ORDER BY UserID;
            """
            run_query(cursor, query, headers=["Username", "Bankroll"])

        # ------------------------------
        # OPTION 2
        # ------------------------------
        elif choice == "2":
            print("\nRunning Query 2: Top 10 bankrolls")
            query = """
                SELECT Username, Bankroll
                FROM UserAccount
                ORDER BY Bankroll DESC
                LIMIT 10;
            """
            run_query(cursor, query, headers=["Username", "Bankroll"])

        # ------------------------------
        # OPTION 3
        # ------------------------------
        elif choice == "3":
            print("\nRunning Query 3: Total bets per user")
            query = """
                SELECT u.Username, COUNT(b.BetID) AS TotalBets
                FROM UserAccount u
                LEFT JOIN Bet b ON u.UserID = b.UserID
                GROUP BY u.UserID
                ORDER BY TotalBets DESC;
            """
            run_query(cursor, query, headers=["Username", "TotalBets"])

        # ------------------------------
        # OPTION 4
        # ------------------------------
        elif choice == "4":
            print("\nRunning Query 4: Average wager per user")
            query = """
                SELECT u.Username, AVG(b.WagerAmount) AS AvgWager
                FROM UserAccount u
                LEFT JOIN Bet b ON u.UserID = b.UserID
                GROUP BY u.UserID
                ORDER BY AvgWager DESC;
            """
            run_query(cursor, query, headers=["Username", "AvgWager"])

        # ------------------------------
        # OPTION 5
        # ------------------------------
        elif choice == "5":
            print("\nRunning Query 5: Last 15 bets placed")
            query = """
                SELECT b.BetID, u.Username, b.BetType, b.WagerAmount, b.Result, b.Payout
                FROM Bet b
                JOIN UserAccount u ON b.UserID = u.UserID
                ORDER BY b.BetID DESC
                LIMIT 15;
            """
            run_query(cursor, query, headers=["BetID", "Username", "Type", "Wager", "Result", "Payout"])

        # ------------------------------
        # OPTION 6
        # ------------------------------
        elif choice == "6":
            print("\nRunning Query 6: Closest games")
            query = """
                SELECT g.GameID, t1.TeamName AS Home, t2.TeamName AS Away,
                       g.HomeScore, g.AwayScore,
                       ABS(g.HomeScore - g.AwayScore) AS ScoreDiff
                FROM Game g
                JOIN Team t1 ON g.HomeTeamID = t1.TeamID
                JOIN Team t2 ON g.AwayTeamID = t2.TeamID
                ORDER BY ScoreDiff ASC
                LIMIT 10;
            """
            run_query(cursor, query, headers=["GameID", "Home", "Away", "HomeScore", "AwayScore", "Diff"])

        # ------------------------------
        # OPTION 7
        # ------------------------------
        elif choice == "7":
            print("\nRunning Query 7: User winnings/losses")
            query = """
                SELECT u.Username,
                       SUM(b.Payout - b.WagerAmount) AS NetResult
                FROM UserAccount u
                LEFT JOIN Bet b ON u.UserID = b.UserID
                GROUP BY u.UserID
                ORDER BY NetResult DESC;
            """
            run_query(cursor, query, headers=["Username", "NetResult"])

        # ------------------------------
        # OPTION 8
        # ------------------------------
        elif choice == "8":
            print("\nRunning Query 8: Team win/loss frequency")
            query = """
                SELECT t.TeamName,
                       SUM(CASE WHEN g.HomeTeamID = t.TeamID AND g.HomeScore > g.AwayScore THEN 1
                                WHEN g.AwayTeamID = t.TeamID AND g.AwayScore > g.HomeScore THEN 1
                                ELSE 0 END) AS Wins,
                       SUM(CASE WHEN g.HomeTeamID = t.TeamID AND g.HomeScore < g.AwayScore THEN 1
                                WHEN g.AwayTeamID = t.TeamID AND g.AwayScore < g.HomeScore THEN 1
                                ELSE 0 END) AS Losses
                FROM Team t
                LEFT JOIN Game g
                ON t.TeamID IN (g.HomeTeamID, g.AwayTeamID)
                GROUP BY t.TeamID
                ORDER BY Wins DESC;
            """
            run_query(cursor, query, headers=["TeamName", "Wins", "Losses"])

        # ------------------------------
        # INVALID OPTION
        # ------------------------------
        else:
            print("\nInvalid choice, try again.\n")

    conn.close()


# ----------------------------------------------
# START PROGRAM
# ----------------------------------------------
if __name__ == "__main__":
    main()
