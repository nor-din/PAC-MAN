*This project has been created as part of the 42 curriculum by nodoulah, nel-mout.*

# PAC-MAN

## Description
A modern Python recreation of PAC-MAN. Built using Pygame and an externally-supplied `A-Maze-ing` (maze generator) package, every level offers a different generated maze with increasing difficulty. The objective is to navigate the maze, collect every pacgum while avoiding four ghosts, each with a unique movement logic. You can also grab a super-pacgum to flip the tables and devour the ghosts for bonus points!

## Instructions
**Installation:**
To set up the required virtual environment and install all dependencies:
```bash
make install
```

**Execution:**
To launch the game with a specific configuration file:
```bash
make run CONFIG=config.json
```
You can also run it manually using a specific configuration file:
```bash
python3 pac-man.py config.json
```

## Resources
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pac-Man Ghost AI Explained](https://www.youtube.com/watch?v=ataGotQ7ir8)
- *AI Usage:* AI was used to help with documentation, linting and debugging.

## Configuration
The game uses a JSON configuration file (e.g., `config.json`) to dictate runtime parameters. The configuration parser supports `#` comments and is built with robust fallback logic using Pydantic. 
- `lives`: Number of player lives (default 3)
- `points_per_pacgum`: Points awarded for eating a regular pacgum (default 10)
- `points_per_super_pacgum`: Points awarded for eating a super pacgum (default 50)
- `points_per_ghost`: Points awarded for eating a frightened ghost (default 200)
- `seed`: Seed for the random number generator to ensure reproducible mazes (default None)
- `level_max_time`: Time limit for the level (default 90)


## Highscore
The highscore system persists data to a local file (`highscore.json`). It keeps track of all scores and players. If the file is missing or corrupted, the system handles the exception gracefully, returning an empty dictionary, and creates a fresh save file at the end of the game.

**Implementation Choice:**
We specifically chose JSON because it natively supports key-value mapping, making it the perfect fit to pair player names (keys) with their scores (values) out of the box. This built-in dictionary structure eliminates the need for manual parsing, allowing us to easily serialize, sort, and update the top 10 scores efficiently. Additionally, JSON files remain completely human-readable, which is a massive benefit for debugging.

## Maze Generation
The mazes are generated using the assigned external `A-Maze-ing` package. We wrap their 2D grid output inside our own `Maze` class, mapping their logical path/wall variables to our rendering coordinate system. The `Maze` class acts as the core spatial authority for the game, interpreting the generator's cell values into traversable paths. It exposes simple APIs like `can_move` for entities to query, completely decoupling the core game logic from the external package's internal data structures.

## Implementation
The game's architecture cleanly separates logical grid coordinates from visual pixel interpolation. The main loop continually processes events (including cheat modes for invincibility, freezing ghosts, and speed boosts) and updates the game state. Entity speeds are decoupled using modulo operations on frame-step counters against configurable "tick" rates. Ghosts rely on a shared global state manager to dynamically switch between "Scatter" and "Chase" modes based on real-time timestamps (`time.time()`), with each ghost executing a unique pathfinding algorithm. Finally, instead of using Pygame's built-in `Rect` hitboxes, all entity interactions (such as eating pacgums or colliding with ghosts) are handled mathematically via pure pixel distance calculations.

## General Software Architecture
The game heavily relies on Object-Oriented Programming (OOP) and is split into modular components that interact systematically:
- **`Game` (`game.py`)**: The central orchestrator. It manages the state machine (menus vs gameplay), initializes the configurations, and loops over all entities to update their logic and trigger rendering.
- **`Player`, `Ghost`, `Pacgum` (`player.py`, `ghost.py`, `pacgum.py`)**: Entity classes. They maintain their own grid logic and pixel interpolation. Ghosts take the `Maze` and `Player` instances as arguments to calculate pathfinding vectors.
- **`Maze` (`maze.py`)**: The spatial authority. Initialized by `Game` and constantly queried by `Player` and `Ghost` classes to validate movement.
- **`GameConfig` (`game_config.py`)**: The configuration parser (Pydantic model), supplying validated parameters globally to the `Game` state.
- **`Images` (`ui.py`)**: A centralized asset loader utilized by the `Game` class to render the HUD and menus.

## Project Management
We divided the workload modularly, tackling distinct classes (e.g., UI vs Ghost AI) to avoid merge conflicts, and utilized pair-programming for complex blocking issues like the configuration parser. 

For a complete breakdown of our process, organization, and decisions, please see our dedicated [Project Management Directory](./project_management/).
