from __future__ import annotations
import json
import src.game


def get_top_ten() -> list[tuple[str, int]]:
    highscores = {}
    filename = src.game.Game.config.highscore_filename
    try:
        with open(filename) as high_score_file:
            highscores = json.load(high_score_file)
    except (FileNotFoundError, json.JSONDecodeError):
        highscores = {}
    hscores = sorted(highscores.items(), key=lambda x: x[1], reverse=True)
    return hscores[:10]
