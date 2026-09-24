# Testing & Quality Assurance (QA)

## Acceptance Test Plan
Our testing strategy involved a mix of manual playtesting for game feel and edge-case testing for system resilience. We intentionally attempted to break the game using faulty configuration files to ensure the application remained stable under improper usage.

### 1. Gameplay Features Tested
We performed extensive manual playtesting to verify the following mechanics:
- **Player Movement & Collisions:** Verified that Pac-Man snaps properly to the grid, does not clip through walls, and wraps around edges if applicable.
- **Ghost State Changes:** Ensured that ghosts properly switch from Chase to Scatter on their internal timers, and correctly transition to Frightened mode (slowing down and reversing direction) when a Super-Pacgum is eaten.
- **Level Progression:** Tested that collecting the final Pacgum correctly triggers the next level sequence, spawns a new maze layout, and increases difficulty parameters like ghost speed.
- **Scoring & Lives:** Confirmed that eating ghosts in Frightened mode grants bonus points, dying resets entities to their spawn points, and losing all lives properly routes to the Game Over/Highscore screen.

### 2. Configuration & Error Handling Tests
To ensure the game never crashes and complies with the "no Python traceback" requirement, we tested the following edge cases during launch:
- **Running without a config file:** (`python3 pac-man.py`) -> *Result:* Handled gracefully via command-line argument checking. Game exits with a clear error message.
- **Running with a non-.json file:** (`python3 pac-man.py config.txt`) -> *Result:* Rejected cleanly. Game prints usage instructions and exits.
- **Corrupted JSON or invalid values:** -> *Result:* The custom parser catches `json.JSONDecodeError` or missing keys, substituting invalid values with safe hardcoded defaults. The game successfully boots using default parameters without tracebacks.

### 3. Bugs Found and Fixed
- **Bug:** Missing highscore files or corrupted score JSON caused a `FileNotFoundError` or `JSONDecodeError` traceback when opening the Highscore menu.
  - **Fix:** Added try/except blocks in `game.py` around the highscore loading function to return an empty dictionary and proceed safely if the file is missing or corrupted.
- **Bug:** Ghosts getting permanently stuck in corners due to pathfinding loops when both horizontal and vertical directions were blocked.
  - **Fix:** Implemented logic to prevent ghosts from reversing their immediate previous direction (`reverse_dir`), forcing them to continue along valid paths.
