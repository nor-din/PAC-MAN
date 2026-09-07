# PAC-MAN: Development Action Plan

## 1. UI Refactoring & Modularity
**Priority: High | Effort: Medium**
- [ ] **Extract UI Logic**: `src/game.py` currently contains a massive amount of hardcoded UI rendering (Main Menu, Instructions, Game Over, Pause menus). Move this logic into the `src/ui.py` file to create a dedicated `UI` class.
- [ ] **Clean Input Handling**: Standardize how inputs are polled (e.g., extracting event handling out of the main game loop into manageable functions).

## 2. Configuration Integration
**Priority: High | Effort: Medium**
- [ ] **Load Config on Boot**: Modify `pac-man.py` so it correctly passes the `config.json` file as an argument into `src/config.py` parser.
- [ ] **Apply Config to Game Variables**: Replace hardcoded values in `game.py` (e.g., `self.time = 90`, `self.player.lives = 3`) with the dynamically loaded configuration dictionary.

## 3. High-Score System
**Priority: Medium | Effort: Medium**
- [ ] **End-Game Prompt**: Implement a text-input field on the Game Over and Victory screens to capture the player's name (max 10 alphanumeric characters).
- [ ] **Save the Score**: Call `HighScoreManager.add_score()` to persistently save the result into `highscores.json`.
- [ ] **Display Top 10**: Render the list of high-scores when the player clicks "Highscores" on the main menu, pulling data from `HighScoreManager.get_top_scores()`.

## 4. Ghost AI (Pathfinding)
**Priority: High | Effort: High**
- [ ] **Chase Logic**: In `src/ghost.py`, replace the `random.choice(directions)` logic with intelligent pathfinding towards the player's coordinates.
- [ ] **Flee Logic**: When ghosts are edible, they must calculate a path that moves *away* from the player's coordinates.

## 5. Level Progression & Difficulty
**Priority: High | Effort: Medium**
- [ ] **Detect Level Completion**: Check if `self.pacgums` is empty. If true, the player wins the level.
- [ ] **Transition State**: Pause the game briefly, increment `self.level`, and use the `config.json` sizes to instantiate a new `MazeGenerator`.
- [ ] **Seed Handling**: Ensure Level 1 uses the seed from the config file, while Levels 2+ use a random seed.
- [ ] **Reset State**: Reset the player's position, ghost positions, and the level timer. Carry over the score and lives.

## 6. Cheat Mode
**Priority: Low | Effort: Low**
- [ ] **Level Skip Cheat**: Map a new key (e.g., `L`) in the event loop that instantly sets the remaining pacgums to 0, triggering the level transition.

## 7. Typing & Linting (Mandatory)
**Priority: High | Effort: Medium**
- [ ] **Add Type Hints**: Add standard Python type hints (`: int`, `-> None`) to function signatures in `game.py`, `maze.py`, `ghost.py`, `pacgum.py`, and `player.py`.
- [ ] **Pass `make lint`**: Run `make lint` frequently and resolve any `flake8` or `mypy` errors to prevent point deductions.

## 8. Final Polish & Deployment
**Priority: Medium | Effort: Low**
- [ ] **Kanban/Timeline**: Document the project timeline and who-did-what in the `project_management/` folder.
- [ ] **Package the Game**: Prepare an executable script or spec that bundles the game for Itch.io/Steam.
