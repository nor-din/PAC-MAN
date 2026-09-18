from __future__ import annotations
import json
import src.game
import pygame


def get_top_ten() -> list[tuple[str, int]]:
    """Reads the highscores JSON and returns the top 10 entries.

    Args:
        None.

    Returns:
        A sorted list of tuples containing (player_name, score).
    """
    highscores = {}
    filename = src.game.Game.config.highscore_filename
    try:
        with open(filename) as high_score_file:
            highscores = json.load(high_score_file)
    except (FileNotFoundError, json.JSONDecodeError):
        highscores = {}
    hscores = sorted(highscores.items(), key=lambda x: x[1], reverse=True)
    return hscores[:10]


def collide_p(x_surf: int, y_surf: int, w: int, h: int) -> bool:
    """Checks if the mouse cursor is hovering over a bounding box.

    Args:
        x_surf: Top-left X coordinate of the box.
        y_surf: Top-left Y coordinate of the box.
        w: Width of the box.
        h: Height of the box.

    Returns:
        True if the mouse is inside the box.
    """
    x, y = pygame.mouse.get_pos()
    if x_surf <= x < x_surf + w and y_surf <= y < y_surf + h:
        return True
    return False
