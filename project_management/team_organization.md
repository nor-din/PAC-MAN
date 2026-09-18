# Team Organization

## Roles and Responsibilities
Our team structured the development workload by dividing major components between two developers. This allowed us to work in parallel, minimize merge conflicts, and leverage our individual strengths.

### nodoulah
- **Game Loop Setup:** Initialized the Pygame engine, managed the frame rate clock, and set up the core event-listening loop.
- **Maze Integration:** Connected the required `A-Maze-ing` package to the game state and extracted the layout data for the renderer.
- **Visuals & Rendering:** Handled the loading of sprites and fonts, mapped the maze generator to pixel coordinates, and rendered all entities.
- **UI & Menus:** Designed and implemented the Start menu, Pause screen, Game Over/Victory screens, and the active HUD (score, lives, timer).
- **Highscore System:** Created the persistent data logic to read, update, sort, and save player highscores to a local JSON file.
- **Player Mechanics:** Programmed Pac-Man's grid-snapping movement, wall collision detection, and the logic for eating standard/super pacgums.
- **Cheat Codes:** Hooked up the keyboard listeners for developer cheats (Freeze, Invincible, Speed, Skip Level) and applied their effects.
- **Deployment to a public gaming platform:** Upload game in itch.io using Pyinsttaler to convert src file to excutable programe, Ex: ./pac-man.py confige.json.


### nel-mout
- **Level Progression:** Developed the logic that triggers when a level is cleared, increases difficulty, and requests a new maze layout.
- **Configuration System:** Built the robust JSON parser, handled command-line argument validation, and ensured faulty configs gracefully fallback without Python tracebacks.
- **Ghost Movement:** Built the base pathfinding and movement rules for ghosts to navigate intersections within the grid.
- **Ghost Behaviors:** Implemented the distinct Chase (targeting algorithms), Scatter (patrolling) and Frightened (edible/slowed) states.
- **Packaging & CLI:** Configured `pyproject.toml`, managed dependencies, and ensured the project could be built and launched properly via command line.
- **Bug Fixing & Edge Cases:** Hunted down gameplay bugs (like sprite clipping) and ensured edge cases were handled without crashing.
- **Project Management & Docs:** Drafted the `README.md`, organized the project management folder, and documented our technical choices and QA plan.

## Decision Making
We used a consensus-based approach for technical decisions. For example, when choosing how to handle configuration failures, we discussed whether to fallback to entirely default files or attempt to salvage partial configurations. We mutually decided on partial salvaging as it provided a better user experience.

## Issue Handling and Conflict Resolution
- **Code Conflicts:** By separating the codebase into distinct modules (`ghost.py`, `ui.py`, `game_config.py`), we minimized git merge conflicts.
- **Blocking Points:** Whenever one of us encountered a roadblock (e.g., how to include the config), we held brief pair-programming sessions to debug the core logic together.
