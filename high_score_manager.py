#!/usr/bin/env python3
"""
High Score Manager for Pacman Game
Command line utility to view and manage high scores
"""
import sys
from high_score_db import HighScoreDB


def main():
    """Main function for high score manager"""
    db = HighScoreDB()

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == 'show' or command == 'list':
        show_top_scores(db)
    elif command == 'info':
        show_database_info(db)
    elif command == 'clear':
        clear_scores(db)
    elif command == 'add':
        add_test_score(db)
    elif command == 'high':
        show_high_score(db)
    else:
        print(f"Unknown command: {command}")
        show_help()


def show_help():
    """Show help information"""
    print("Pacman High Score Manager")
    print("=" * 25)
    print("Usage: python3 high_score_manager.py <command>")
    print("")
    print("Commands:")
    print("  show/list  - Show top 10 scores")
    print("  high       - Show current high score")
    print("  info       - Show database statistics")
    print("  add        - Add a test score")
    print("  clear      - Clear all scores (WARNING: Cannot be undone)")
    print("")


def show_top_scores(db, limit=10):
    """Show top scores"""
    scores = db.get_top_scores(limit)

    if not scores:
        print("No scores recorded yet!")
        return

    print(f"*** Top {min(len(scores), limit)} Scores ***")
    print("=" * 50)

    for i, score_data in enumerate(scores, 1):
        rank_display = f"{i}"
        print(f"{rank_display:>4} {score_data['score']:>6} pts  {score_data['player']:<12} ({score_data['date']})")


def show_high_score(db):
    """Show current high score with details"""
    info = db.get_high_score_info()

    print("Current High Score:")
    print("=" * 22)
    print(f"Score: {info['score']} points")
    print(f"Player: {info['player']}")
    print(f"Date: {info['date']}")


def show_database_info(db):
    """Show database statistics"""
    info = db.get_database_info()

    print("Database Information:")
    print("=" * 24)
    print(f"Total games played: {info['total_games']}")
    print(f"Average score: {info['average_score']}")
    print(f"Database file: {info['database_file']}")

    high_score_info = db.get_high_score_info()
    print(f"High score: {high_score_info['score']} pts")


def clear_scores(db):
    """Clear all scores with confirmation"""
    response = input("️Are you sure you want to clear ALL scores? (yes/no): ")

    if response.lower() == 'yes':
        if db.clear_scores():
            print("All scores cleared successfully!")
        else:
            print("Error clearing scores.")
    else:
        print("Operation cancelled.")


def add_test_score(db):
    """Add a test score"""
    try:
        score_input = input("Enter test score: ")
        score = int(score_input)

        player_name = input("Enter player name (or press Enter for 'TestPlayer'): ").strip()
        if not player_name:
            player_name = "TestPlayer"

        is_new_high = db.update_high_score(score, player_name)

        if is_new_high:
            print(f"NEW HIGH SCORE! {score} points by {player_name}")
        else:
            print(f"Score added: {score} points by {player_name}")

    except ValueError:
        print("Invalid score. Please enter a number.")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")


if __name__ == "__main__":
    main()