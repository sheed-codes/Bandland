import random
import mysql.connector

# -------------------------
# CONNECT TO BANDLAND
# -------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bandland"
)
cursor = conn.cursor()
print("Connected to BANDLAND…")

# -------------------------
# INSERT USERS
# -------------------------
gamertags = [
    "IceWolf","ShadowReaper","KingSlayer","RazorEdge","NightHawk",
    "StormBreaker","TurboViper","IronSteel","MysticFlare","BlazeShot",
    "BlueDragon","SilentGhost","FutureShock","TriggerHappy","HeatSeeker",
    "FadeAway","ClutchMaster","NetBreaker","GridIronGod","SkyWalker",
    "ApexPredator","SniperWolf","GhostRider","LaserHawk","NovaPrime",
    "Deadshot","LightningBolt","CrimsonStrike","Blackout","VortexZX",
    "AlphaWolf","OmegaStrike","PhantomKing","ThunderFlash","FrostByte",
    "WildCard","SteelTitan","GoldenKnight","StormChaser","BlueComet",
    "IronClaw","TheEqualizer","Hurricane","TheEnforcer","RogueOne",
    "TidalWave","ShockWave","SilverBullet","PrimeTime","LockDown",
    "Maverick","LethalShot","ColdBlooded","IronFist","BigChief",
    "AirRusher","MegaMind","BeastMode","Ruthless","SavageKing",
    "KickReturner","DeepThreat","FieldGeneral","RouteRunner","BallHawk",
    "DunkMaster","SkyHigh","Posterizer","TripleDouble","BucketsOnly",
    "Sharpshooter","SplashZone","IsoGod","PickNRoll","CrashBoard",
    "PaintBeast","TwoWayFinisher","ClampGod","LockdownDemon","BreakStarter",
    "FlashDrive","QuickStrike","FireStorm","RumblePack","SilentHunter",
    "JetStream","DarkMatter","BlueMagic","TheAnswer","BlackMamba24",
    "WindRunner","IceCold","NoChill","HighVoltage","GameBreaker",
    "RookieOfTheYear","VeteranStatus","FinalBoss","UnderDog","SuperNova",
    "TheProdigy","TheChosenOne","ReignMaker","DynastyMode","AllStar"
]

cursor.executemany(
    "INSERT INTO UserAccount (Username) VALUES (%s)",
    [(tag,) for tag in gamertags]
)

conn.commit()

cursor.execute("SELECT UserID FROM UserAccount")
users = [u[0] for u in cursor.fetchall()]
print(f"Inserted {len(users)} users")

# -------------------------
# INSERT TEAMS
# -------------------------
teams = [
    ("Los Angeles Lakers","NBA"), ("Chicago Bulls","NBA"),
    ("Boston Celtics","NBA"), ("Miami Heat","NBA"),
    ("Golden State Warriors","NBA"), ("Milwaukee Bucks","NBA"),
    ("Phoenix Suns","NBA"), ("Dallas Mavericks","NBA"),
    ("New York Knicks","NBA"), ("Philadelphia 76ers","NBA"),

    ("Chicago Bears","NFL"), ("Green Bay Packers","NFL"),
    ("Kansas City Chiefs","NFL"), ("Buffalo Bills","NFL"),
    ("Dallas Cowboys","NFL"), ("San Francisco 49ers","NFL"),
    ("Philadelphia Eagles","NFL"), ("Miami Dolphins","NFL"),
    ("Baltimore Ravens","NFL"), ("Detroit Lions","NFL")
]

cursor.executemany(
    "INSERT INTO Team (TeamName, League) VALUES (%s,%s)",
    teams
)
conn.commit()

cursor.execute("SELECT TeamID, TeamName FROM Team")
team_list = cursor.fetchall()
print(f"Inserted {len(team_list)} teams")

# -------------------------
# INSERT GAMES
# -------------------------
games = []

# 20 NBA games
for i in range(20):
    home = random.randint(1, 10)
    away = random.randint(1, 10)
    while away == home:
        away = random.randint(1, 10)

    games.append((home, away, "2024-01-{:02d}".format(i+1),
                  random.randint(90, 130), random.randint(85, 125), "NBA"))

# 20 NFL games
for i in range(20):
    home = random.randint(11, 20)
    away = random.randint(11, 20)
    while away == home:
        away = random.randint(11, 20)

    games.append((home, away, "2024-09-{:02d}".format(i+1),
                  random.randint(10, 35), random.randint(10, 35), "NFL"))

cursor.executemany("""
    INSERT INTO Game (HomeTeamID, AwayTeamID, GameDate, HomeScore, AwayScore, League)
    VALUES (%s,%s,%s,%s,%s,%s)
""", games)

conn.commit()

cursor.execute("SELECT GameID, HomeScore, AwayScore FROM Game")
games = cursor.fetchall()
print(f"Inserted {len(games)} games")

# -------------------------
# INSERT RANDOM BETS
# -------------------------
bet_count = 0

for user in users:
    for _ in range(4):

        game_id, hscore, ascore = random.choice(games)
        pick = random.choice(["HOME","AWAY"])
        wager = round(random.uniform(5,50),2)
        odds = round(random.uniform(1.2,3.5),2)

        result = "WIN" if (pick == "HOME" and hscore > ascore) or (pick == "AWAY" and ascore > hscore) else "LOSS"
        payout = round(wager * odds,2) if result == "WIN" else 0.00
        net = payout - wager

        cursor.execute("""
            INSERT INTO Bet (UserID, GameID, BetType, WagerAmount, Pick, Result, Odds, Payout)
            VALUES (%s,%s,'MONEYLINE',%s,%s,%s,%s,%s)
        """, (user, game_id, wager, pick, result, odds, payout))

        cursor.execute("""
            UPDATE UserAccount SET Bankroll = Bankroll + %s WHERE UserID = %s
        """, (net, user))

        cursor.execute("""
            INSERT INTO TransactionLog (UserID, Amount, Type)
            VALUES (%s,%s,'Bet Result')
        """, (user, net))

        bet_count += 1

conn.commit()
print(f"Inserted {bet_count} bets.")
print("DONE!")
