import sqlite3

class Database:

    def __init__(self):
        connection = sqlite3.connect("word_of_the_day.db")
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS words ("
            "id INTEGER PRIMARY KEY, word TEXT, meaning TEXT, example TEXT)"
        )
        connection.commit()
        
    def insert(connection, word, meaning, example):
        connection = sqlite3.connect("word_of_the_day.db")
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM words WHERE word=?', (word, ))
        entry = cursor.fetchone()

        print(entry)

        if entry is None:
            cursor.execute("INSERT INTO words (word, meaning, example) VALUES(?, ?, ?)", (word, meaning, example))
            connection.commit()
            connection.close()
    
    def delete(connection, word):
        connection = sqlite3.connect("word_of_the_day.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM words WHERE word = ?", (word,))
        connection.commit()
        connection.close()
