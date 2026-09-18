# Project Analysis & Technical Choices

## Architectural Decisions
The overall architecture of the game is based on object-oriented programming (OOP). We separated the game into distinct modules to maintain a clean codebase and ease collaboration:
- **Game Engine**: `game.py` handles the main loop, event processing, and ties all entities together.
- **Entities**: `player.py`, `ghost.py`, and `pacgum.py` manage the state and logic for individual game objects.
- **Configuration**: `game_config.py` is entirely separated from the game logic, ensuring parsing errors are handled securely before Pygame initializes.
- **UI & Helpers**: `ui.py` and `utils.py` encapsulate drawing functions, fonts, menus, and file I/O for the highscore.

This modularity made bug fixing easier since rendering problems were isolated from pathfinding or state mechanics.

## Technical Choices

### 1. Pygame for Rendering and Events
- **Choice:** We used Pygame as the primary engine for rendering, user inputs, and time management.
- **Reasoning:** Pygame is standard, stable, and perfectly suited for a 2D tile-based arcade game like Pac-Man. It provides straightforward methods for rendering images and handling keyboard inputs while matching the requirements for an MLX-equivalent graphical library.

### 2. Custom JSON Parsing for Configuration
- **Choice:** Implemented a robust fallback system in `game_config.py` for parsing the `config.json` file.
- **Reasoning:** The subject requires the program to never crash on a faulty config. By manually handling the JSON decoding and validating keys, we can guarantee that missing, corrupted, or mistyped keys automatically revert to safe default values without tracebacks.

### 3. State-based AI Architecture
- **Choice:** Ghosts dynamically update their movement logic between Scatter, Chase, and Frightened states using shared class variables and function pointers.
- **Reasoning:** This closely emulates the original Pac-Man ghost logic and provides an extensible foundation. Each ghost can have a unique targeting function (e.g., `chase_pink` vs `chase_red`) while still sharing the generic intersection-navigation codebase.

## Risk Analysis & Mitigation
- **Risk:** Python tracebacks from faulty or missing configuration files causing the game to crash.
  - **Mitigation:** Used `try/except` blocks during the JSON loading phase and validated all parsed values against hardcoded fallbacks to guarantee the game always boots successfully.
- **Risk:** The external `mazegenerator` package failing or returning unpredictable layouts.
  - **Mitigation:** We encapsulated the maze loading logic in `maze.py`, adapting their generated 2D grid into our own coordinate space. This decouples our game loop from their specific data structures.
- **Risk:** Infinite loops during ghost pathfinding or floating point inaccuracies in visual movement.
  - **Mitigation:** Separated logical coordinates (row/col) from visual coordinates (x/y), applying pixel adjustments dynamically. Ghost movement restricts valid turns and prevents reversing direction to avoid getting stuck in loops.
