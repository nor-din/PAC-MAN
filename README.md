*This project has been created as part of the 42 curriculum by nodoulah, nel-mout.*

# PAC-MAN

## Description
A modern Python implementation of the classic PAC-MAN arcade game. The objective is to eat all pacgums in the maze without being caught by the ghosts. Collect Super-Pacgums to turn the tables and eat the ghosts for bonus points! 

## Instructions
**Installation:**
```bash
make install
```

**Execution:**
```bash
make run CONFIG=config.json
```
You can also run it manually using a configuration file:
```bash
python3 pac-man.py config.json
```

**Controls:**
- **Movement:** Arrow keys

## Configuration
The game uses a `config.json` file to dictate parameters. The configuration parser supports C-style `#` comments and is built with robust fallback logic using Pydantic. 
- `lives`: Number of player lives (default 3)
- `level_max_time`: Time limit for the level (default 90)
- `points_per_ghost`: Points awarded for eating a frightened ghost.
- `ghost_respawn_ms`: Milliseconds a ghost stays dead before respawning.

*TODO: Add any other custom config keys you want to highlight here.*

## Highscore
The highscore system persists data to a local `highscore.json` file. It keeps track of the top 10 scores and players. If the file is missing or corrupted, the system handles the exception gracefully, returning an empty dictionary, and creates a fresh save file at the end of the game.

## Maze Generation
The mazes are generated using the external `A-Maze-ing` package assigned to us. We wrap their 2D grid output in our `Maze` class, mapping their logical path/wall variables to our rendering coordinate system, making it completely decoupled from their internal code. 

## Implementation
The game loop runs at 60 FPS using Pygame for rendering and events. The logic updates based on frame-tick counters for speed control. Collisions are handled logically using the grid matrix rather than physical hitboxes, ensuring perfect alignment.

## General Software Architecture
The game heavily relies on Object-Oriented Programming (OOP) and is split into modular components:
- `game.py`: The core state machine and game loop.
- `ghost.py`, `player.py`, `pacgum.py`: Entity classes managing their respective visual and logical states.
- `maze.py`: Wrapper for the maze generator data.
- `game_config.py`: The decoupled JSON parser.
- `ui.py`: Asset loader and menu renderer.

## Project Management
Project management documentation can be found in the `project_management/` folder. It contains:
- `analysis_and_choices.md`: Our architectural decisions.
- `progress.md`: Our iterative task tracking.
- `team_organization.md`: How we split tasks and resolved conflicts.
- `testing_and_qa.md`: Our QA plan and bug fixes.

## Resources
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- *AI Usage:* AI was used to generate comprehensive docstrings across the codebase and assist in debugging configuration timing logic (converting ms to seconds).
