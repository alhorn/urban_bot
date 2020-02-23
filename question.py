import random
import sqlite3

class Question:
    def __init__(self):
        self.word = ''
        self.options = []
        self.answer = 0
    
    def get_questions(self):
        conn = sqlite3.connect("urban_db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT rowid, word, word_def from Words ORDER BY RANDOM() LIMIT 1") 
        key_word = cursor.fetchall()
        self.word = key_word[0][1]

        cursor.execute("SELECT word_def from Words where rowid != {} ORDER BY RANDOM() LIMIT 3".format(str(key_word[0][0]))) 
        rnd_def = cursor.fetchall()

        rnd_def.append([key_word[0][2]])
        random.shuffle(rnd_def)

        self.options = rnd_def

        for i in range(len(rnd_def)):
            if rnd_def[i][0] == key_word[0][2]:
                self.answer = i
                break