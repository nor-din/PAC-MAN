# Project Progress & Retrospective

## Overview
This document tracks the actual progress of the PAC-MAN project across different development phases. Since we adopted an iterative approach, our progress was tracked based on feature completion and assigned responsibilities.

## Phase Tracking

| Phase | Description / Goal | nodoulah's Tasks | nel-mout's Tasks | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Foundation & Setup**<br>Establish the core engine, integrate the maze generator, and set up the robust configuration system. | - Game Loop Setup<br>- Maze Integration | - Configuration System | Completed | Successfully laid the groundwork for rendering and safe data parsing without tracebacks. |
| **Phase 2** | **Core Mechanics & Movement**<br>Implement rendering, player controls, collisions, and base ghost navigation. | - Visuals & Rendering<br>- Player Mechanics | - Ghost Movement | Completed | Achieved smooth grid-snapping for Pac-Man and established pathfinding logic for the ghosts. |
| **Phase 3** | **Logic, UI & AI Behaviors**<br>Flesh out distinct ghost states, menus, and persistent data tracking. | - UI & Menus<br>- Highscore System | - Ghost Behaviors | Completed | UI screens linked successfully. Ghost AI switches correctly between Chase, Scatter, and Frightened. |
| **Phase 4** | **Polish, Delivery & QA**<br>Finalize level progression, developer cheats, bug fixes, packaging, and documentation. | - Cheat Codes<br>- Deployment | - Level Progression<br>- Packaging & CLI<br>- Bug Fixing & Edge Cases<br>- Project Management & Docs | Completed | Handled all edge cases. Project builds successfully via `pyproject.toml` and documentation is complete. |
