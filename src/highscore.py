import json


import src.game

def get_top_ten():
    highscores = {}
    
    filename = src.game.Game.config_dict.get("highscore_filename", "highscore.json")
    try:
        with open(filename) as high_score_file:
            highscores = json.load(high_score_file)
    except FileNotFoundError:
        highscores = {}

    highscores = [(name, score) for name, score in highscores.items()]

    if len(highscores) <= 10:
        return highscores
    else:
        return highscores[:10]
