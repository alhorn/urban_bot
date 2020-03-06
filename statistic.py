import sqlite3
import math

def stat_insert(a):
    conn = sqlite3.connect("statistic.db")
    cursor = conn.cursor()  
    cursor.execute("SELECT user_id FROM Users where user_id = {}".format(a[0]))
    if len(cursor.fetchall()) == 0:
        cursor.execute("INSERT INTO Users VALUES(?, ?, ?, ?)", a)
        conn.commit()
    else:
        cursor.execute("""UPDATE Users SET total_games = total_games + {},
        total_correct = total_correct + {}, 
        total_wrong = total_wrong + {}
        WHERE user_id = {}""".format(a[1], a[2], a[3], a[0]))
        conn.commit()


def get_stats(message):
    conn = sqlite3.connect("statistic.db")
    cursor = conn.cursor()
    text = ''  
    cursor.execute("SELECT * FROM Users where user_id = {}".format(message.from_user.id))
    stats = cursor.fetchall()
    if len(stats) != 0:
        text += "Your stats:\nGames played: {}\nCorrect answers: {}({}%)\nWrong answers: {}({}%)\n".format(
            stats[0][1], stats[0][2], math.ceil(stats[0][2] / (stats[0][2] + stats[0][3]) * 100), stats[0][3],
            100 - math.ceil(stats[0][2] / (stats[0][2] + stats[0][3]) * 100))

        return text
    else:
        text = "You don't played yet"
        return text