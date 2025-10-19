# Pac-Man Game

## Description
This project is a Python implementation of the classic arcade game Pac-Man. Utilizing the Pygame library, it recreates the nostalgic experience of the original game with a modern touch. Players can navigate through mazes, collect points, and avoid ghosts in a quest to clear the levels.

## Demo

![pacman](https://github.com/GurpreetSingh97/Pacman/assets/36395745/d5687d0d-6011-4fef-a1a6-2f036b0dc4f9)

## New Features Added

### 🔊 Sound Effects
- Chomp sounds when eating pellets
- Death sound when caught by ghosts
- Special sounds for eating ghosts and power-ups
- Game start sound

### ⏸️ Pause System
- Press **P** or **ESC** to pause the game
- Pause menu with options:
  - Resume Game
  - Start New Game
  - View High Scores
  - Quit Game

### 🏆 High Score System
- Automatic score saving to local database
- Top 10 leaderboard with player names
- Name entry for top 10 scores
- High score display during gameplay
- "NEW HIGH SCORE!" message

### 📊 Database Features
- SQLite database for storing scores
- Command-line tool for managing scores: `python3 high_score_manager.py`
- View scores, clear database, add test scores

### 🎮 Enhanced Gameplay
- Lives display at bottom of screen
- Current score and high score shown during play
- Better game over screen with full leaderboard
- Improved user interface

## Requirements
- Python 3.x
- Pygame

## Installation
1. Clone the repository: ```git clone https://github.com/GurpreetSingh97/Pacman.git ```
2. Install Pygame: ```pip install pygame```

## Usage
Run the game by executing the `pacman.py` file: ```python pacman.py```

### Game Controls
- **Arrow Keys** - Move Pacman
- **P** or **ESC** - Pause/Resume game
- **SPACE** - Restart after game over
- **ENTER** - Select menu options

### High Score Management
View your scores: ```python3 high_score_manager.py show```
See all available commands: ```python3 high_score_manager.py```
