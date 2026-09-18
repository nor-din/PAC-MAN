*This project has been created as part of the 42 curriculum by nodoulah, nel-mout.*

# PAC-MAN

## Description
A modern Python recreation of PAC-MAN. Built using Pygame and an externally-supplied `A-Maze-ing` (maze generator), every level offers a different generated maze with increasing difficulty. The objective is to navigate the maze, collect every pacgum while avoiding four ghosts. Each with a unique movement logic. but you can grab a super-pacgum to flip the tables and devour the ghosts for bonus points!

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

## Resources
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pac-Man Ghost AI Explained](https://www.youtube.com/watch?v=ataGotQ7ir8)
- *AI Usage:* AI was used to help with documentation and debugging.

## Configuration
The game uses a `config.json` file to dictate parameters. The configuration parser supports `#` comments and is built with robust fallback logic using Pydantic. 
- `lives`: Number of player lives (default 3)
- `level_max_time`: Time limit for the level (default 90)
- `points_per_ghost`: Points awarded for eating a frightened ghost.
- `ghost_respawn_ms`: Milliseconds a ghost stays dead before respawning.
- `points_per_pacgum`: Points awarded for eating a regular pacgum (default 10).
- `points_per_super_pacgum`: Points awarded for eating a super pacgum (default 50).
- `seed`: Seed for the random number generator to ensure reproducible mazes (default None).


## Highscore
The highscore system persists data to a local `highscore.json` file. It keeps track of all scores and players. If the file is missing or corrupted, the system handles the exception gracefully, returning an empty dictionary, and creates a fresh save file at the end of the game.

**Why JSON?**
We specifically chose JSON because it natively supports key-value mapping, making it the perfect fit to pair player names (keys) with their scores (values) out of the box. This built-in dictionary structure eliminates the need for manual parsing, allowing us to easily serialize, sort, and update the top scores. Additionally, JSON files remain completely human-readable, which is a massive benefit for debugging.

## Maze Generation
The mazes are generated using the external `A-Maze-ing` package assigned to us. We wrap their 2D grid output in our `Maze` class, mapping their logical path/wall variables to our rendering coordinate system. The `Maze` class acts as the core spatial authority, utilizing bitwise operations to interpret the generator's cell values into traversable paths. It provides simple methods like `can_move` for entities to query, completely decoupling the game logic from the external package's internal data structures.

## Implementation
The game's architecture cleanly separates logical grid coordinates from visual pixel interpolation. The main loop continually processes events (including cheat modes for invincibility, freezing ghosts, and speed boosts) and updates game state. Entity speeds are decoupled using modulo operations on frame-step counters against configurable "tick" rates. Ghosts rely on a shared global state manager to dynamically switch between "Scatter" and "Chase" modes based on real-time timestamps (`time.time()`), with each ghost executing a unique pathfinding algorithm. Finally, instead of using Pygame's built-in `Rect` hitboxes, all entity interactions (such as eating pacgums or colliding with ghosts) are handled mathematically via pixel distance calculations.

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
- `testing_and_qa.md`: Our quality assurance plan and bug fixes.
