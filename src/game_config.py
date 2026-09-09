"""Game constants for easy modification."""

from pathlib import Path
import json


def is_valid(key, value):
    numeric_set = {
        "lives",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "level_max_time",
        "ghost_respawn_ms",
        "super_pacgum_duration_ms",
        "scatter_duration_ms",
        "chase_duration_ms"
    }

    if key == "highscore_filename":
        if not isinstance(value, str) or not value:
            return False

        path = Path(value)

        if path.exists() and not path.is_file():
            return False

        if not path.parent.exists():
            return False

        return True

    elif key in numeric_set:
        if not isinstance(value, int) or isinstance(value, bool):
            return False

        if value <= 0:
            return False

        return True

    elif key == "seed":
        return value is None or isinstance(value, (int, float, str))

    return False


def remove_comments(lines):
    clean_lines = []

    for line in lines:
        clean_lines.append(line.partition('#')[0])

    return "\n".join(clean_lines)


def parse_config(filename: str):
    config_dict = {
        "highscore_filename": "highscore.json",
        "lives": 3,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": None,
        "level_max_time": 90,

        # Maze Dimensions
        "maze_rows": 15,
        "maze_cols": 15,

        # Game Logic
        "fps": 60,

        # Speeds & Debugging
        "player_speed_ticks": 10,
        "ghost_speed_ticks": 30,
        "player_default_move": 1,
        "player_cheat_move": 2,

        # Timers
        "ghost_respawn_ms": 8000,
        "super_pacgum_duration_ms": 7000,
        "scatter_duration_ms": 7000,
        "chase_duration_ms": 20000
    }

    allowed_keys = {
        "highscore_filename",
        "lives",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "seed",
        "level_max_time",
        "ghost_respawn_ms",
        "super_pacgum_duration_ms",
        "scatter_duration_ms",
        "chase_duration_ms"
    }

    try:
        with open(filename, 'r') as config_file:
            cleaned_file = remove_comments(config_file.readlines())
            user_config = json.loads(cleaned_file)

        # Override defaults with valid user inputs
        for key in config_dict:
            if key in user_config and key in allowed_keys and is_valid(key, user_config[key]):
                config_dict[key] = user_config[key]
    except FileNotFoundError:
        print(f"Warning: Config file '{filename}' not found. Using defaults.")
    except PermissionError:
        print(f"Warning: Permission denied for config file '{filename}'. Using defaults.")
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON in config file '{filename}': {e}. Using defaults.")
    except Exception as e:
        print(f"Warning: Error reading config file '{filename}': {e}. Using defaults.")

    return config_dict

