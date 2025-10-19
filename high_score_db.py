"""
High Score Database for Pacman Game
Simple SQLite database to store and retrieve the highest score
"""
import sqlite3
import os
from datetime import datetime


class HighScoreDB:
    """Manages high score storage using SQLite"""

    def __init__(self, db_path="pacman_scores.db"):
        """Initialize the high score database"""
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Create the high score table if it doesn't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS high_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER NOT NULL,
                    date_achieved TEXT NOT NULL,
                    player_name TEXT DEFAULT 'Player'
                )
            ''')

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(f"Database error during initialization: {e}")

    def get_high_score(self):
        """Get the current high score"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT MAX(score) FROM high_scores')
            result = cursor.fetchone()

            conn.close()

            # Return 0 if no scores exist yet
            return result[0] if result[0] is not None else 0

        except sqlite3.Error as e:
            print(f"Database error getting high score: {e}")
            return 0

    def get_high_score_info(self):
        """Get detailed high score information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT score, date_achieved, player_name
                FROM high_scores
                WHERE score = (SELECT MAX(score) FROM high_scores)
                ORDER BY date_achieved DESC
                LIMIT 1
            ''')
            result = cursor.fetchone()

            conn.close()

            if result:
                return {
                    'score': result[0],
                    'date': result[1],
                    'player': result[2]
                }
            else:
                return {
                    'score': 0,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'player': 'Player'
                }

        except sqlite3.Error as e:
            print(f"Database error getting high score info: {e}")
            return {'score': 0, 'date': 'Unknown', 'player': 'Player'}

    def save_score(self, score, player_name="Player"):
        """Save a new score to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            date_achieved = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                INSERT INTO high_scores (score, date_achieved, player_name)
                VALUES (?, ?, ?)
            ''', (score, date_achieved, player_name))

            conn.commit()
            conn.close()

            return True

        except sqlite3.Error as e:
            print(f"Database error saving score: {e}")
            return False

    def is_new_high_score(self, score):
        """Check if the given score is a new high score"""
        current_high = self.get_high_score()
        return score > current_high

    def is_top_10_score(self, score):
        """Check if the given score qualifies for top 10"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get the 10th highest score
            cursor.execute('''
                SELECT score FROM high_scores
                ORDER BY score DESC
                LIMIT 10
            ''')
            results = cursor.fetchall()
            conn.close()

            # If we have less than 10 scores, or this score beats the 10th place
            if len(results) < 10:
                return True
            elif len(results) == 10 and score > results[9][0]:
                return True
            else:
                return False

        except sqlite3.Error as e:
            print(f"Database error checking top 10: {e}")
            return False

    def update_high_score(self, score, player_name="Player"):
        """Update high score if the new score is higher"""
        if self.is_new_high_score(score):
            self.save_score(score, player_name)
            return True
        else:
            # Still save the score for history, but it's not a new high
            self.save_score(score, player_name)
            return False

    def get_top_scores(self, limit=10):
        """Get top scores for leaderboard"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT score, date_achieved, player_name
                FROM high_scores
                ORDER BY score DESC, date_achieved DESC
                LIMIT ?
            ''', (limit,))

            results = cursor.fetchall()
            conn.close()

            return [{'score': row[0], 'date': row[1], 'player': row[2]} for row in results]

        except sqlite3.Error as e:
            print(f"Database error getting top scores: {e}")
            return []

    def clear_scores(self):
        """Clear all scores (for testing or reset)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM high_scores')

            conn.commit()
            conn.close()

            return True

        except sqlite3.Error as e:
            print(f"Database error clearing scores: {e}")
            return False

    def get_database_info(self):
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM high_scores')
            total_games = cursor.fetchone()[0]

            cursor.execute('SELECT AVG(score) FROM high_scores')
            avg_score = cursor.fetchone()[0] or 0

            conn.close()

            return {
                'total_games': total_games,
                'average_score': round(avg_score, 1),
                'database_file': self.db_path
            }

        except sqlite3.Error as e:
            print(f"Database error getting info: {e}")
            return {'total_games': 0, 'average_score': 0, 'database_file': self.db_path}