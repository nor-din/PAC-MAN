import json
import os
from typing import Any, Dict, cast


def load_config(filepath: str) -> Dict[str, Any]:
    """
    Loads a JSON configuration file that may contain comments.
    Comments starting with '#' are ignored.
    If the file is missing or invalid, a safe default configuration is returned.
    """
    default_config = {
        "highscore_filename": "highscores.json",
        "lives": 3,
        "level_max_time": 90,
        "seed": 42,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "levels": [{"width": 15, "height": 15} for _ in range(10)],
    }

    if not os.path.exists(filepath):
        print(f"Warning: Configuration file '{filepath}' not found. Using defaults.")
        return default_config

    try:
        with open(filepath, "r") as file:
            lines = file.readlines()

        # Remove comments starting with #
        cleaned_lines = []
        for line in lines:
            if "#" in line:
                line = line.split("#")[0]
            cleaned_lines.append(line)

        cleaned_json = "".join(cleaned_lines)
        config = json.loads(cleaned_json)

        # Merge with defaults to ensure all keys exist
        for key, value in default_config.items():
            if key not in config:
                config[key] = value

        return cast(Dict[str, Any], config)

    except Exception as e:
        print(f"Warning: Failed to parse '{filepath}' ({e}). Using defaults.")
        return default_config
