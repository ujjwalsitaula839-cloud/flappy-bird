import sqlite3
import datetime

def get_db_connection():
    try:
        return sqlite3.connect('flappy_scores.db')
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_table():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS high_score (
                    id INTEGER PRIMARY KEY,
                    score INTEGER NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            conn.commit()
            conn.close()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def save_score(score):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('SELECT score FROM high_score LIMIT 1')
            current_high = cursor.fetchone()

            if current_high is None:
                cursor.execute('INSERT INTO high_score (id, score, date) VALUES (1, ?, ?)', (score, date_str))
            elif score > current_high[0]:
                cursor.execute('UPDATE high_score SET score = ?, date = ? WHERE id = 1', (score, date_str))

            conn.commit()
            conn.close()
    except sqlite3.Error as e:
        print(f"Error saving score: {e}")

def get_high_score():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT score FROM high_score LIMIT 1')
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        return 0
    except sqlite3.Error as e:
        print(f"Error getting high score: {e}")
        return 0
