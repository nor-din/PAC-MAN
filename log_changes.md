# Architectural Refactoring Logs

This document tracks the major architectural changes made to clean up the codebase. 

## 1. Constants & State Machine Introduction
- **Created `src/constants.py`**: Added a `GameState` Enum (`MENU`, `INSTRUCTIONS`, `PLAYING`, `PAUSED`, `GAME_OVER`).
- **Refactored `game.py`**: Removed the nested, fragile `while` loops (`while self.run_game`, `while self.run_menu`). Replaced them with a single `while self.running:` loop at the top level that switches its logic based on `self.state`. This prevents stack overflows and makes the game flow crystal clear.

## 2. Asset Manager & Dynamic Scaling
- **Problem Fixed**: Previously, every Ghost, Pacgum, and Player loaded their PNGs directly from the hard drive (`pygame.image.load`) every time they spawned. Additionally, the cell size (`40` pixels) was hardcoded everywhere, meaning Level 10 (33x33) would overflow the 1000x1000 screen limit.
- **Solution**: 
  - Created an `AssetManager` in `src/ui.py`.
  - Added a method `scale_level_assets(cell_size)` which pre-scales and caches all game sprites for the current level's specific grid size.
  - Entities no longer touch the hard drive; they just ask `AssetManager` for their image.
  - `game.py` now dynamically calculates the maximum `cell_size` and `offsets` based on the current maze dimensions so the game perfectly fits the 1000x1000 window, regardless of how big the maze gets!

## 3. Decoupling Logic from Rendering
- **Problem Fixed**: Entities like `Ghost` and `Player` had `self.col * 40 + 200` hardcoded in their `draw` methods, mixing physical screen pixels with game logic.
- **Solution**: 
  - Entities now only store their logical `row` and `col` grid positions.
  - The `draw(screen, assets, cell_size, offset_x, offset_y)` methods now receive exactly where they should be drawn from the main game loop, completely separating game math from Pygame rendering.
