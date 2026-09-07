> *This project has been created as part of the 42 curriculum by nel-mout.*

# Pacman

## Description
A modern Python recreation of the famous 1980 arcade game Pac-Man. This project utilizes Object-Oriented Programming and `pygame` to deliver a robust game engine supporting custom JSON configurations, a persistent highscore system, random maze generation, and various cheat modes for testing.

## Instructions
**Installation**
1. Ensure you have Python 3.10+ installed.
2. Run `make install` to install dependencies.

**Execution**
Launch the game by providing a configuration file:
```bash
make run
```
Or manually:
```bash
uv run python3 pac-man.py config.json
```

## Configuration
The game is configured via a JSON file (`config.json`) which supports comments using `#`. 
If a key is missing or invalid, safe default values are automatically used to prevent crashes.
- `highscore_filename`: Path to save the highscores.
- `lives`: Number of starting lives.
- `level_max_time`: Maximum time per level in seconds.
- `seed`: Random generation seed for the first level.
- `levels`: An array specifying the width and height of each consecutive level.

## Highscore
The highscore system saves top players directly to a local JSON file (`highscores.json`). It persists across game sessions. The game maintains the top 10 scores and prompts the player to enter a maximum 10-character alphanumeric name at the game-over screen. This approach was chosen for simplicity, zero external database requirements, and ease of portability.

## Maze Generation
The mazes are generated dynamically using the `mazegenerator` package provided. Level 1 uses a fixed seed to ensure consistent starting conditions, while subsequent levels increase in size and are generated randomly.

## Implementation
The game relies heavily on `pygame` for rendering the graphical interface and handling game ticks. All states (menus, game, game-over) are encapsulated within a central `Game` loop.

## General Software Architecture
- **`pac-man.py`**: The entry point of the game.
- **`src/config.py`**: A robust JSON parser that handles comments and default values.
- **`src/game.py`**: Manages the main game loop, UI rendering, and entity interactions.
- **`src/ghost.py` / `src/player.py`**: Contains entity-specific logic, rendering, and pathfinding.
- **`src/highscore.py`**: Manages I/O for saving and retrieving top scores.
- **`src/maze.py`**: An abstraction layer mapping the `mazegenerator` outputs to Pygame drawing and collision checks.

## Project Management
Project management artifacts, including timelines and task distribution, can be found in the `project_management/` directory.

## Resources
- [Pygame Documentation](https://www.pygame.org/docs/)
- AI Usage: AI was primarily used for scaffolding boilerplate files (Makefile, Configuration parser, and README structuring), allowing the team to focus entirely on core game mechanics and ghost pathfinding.
