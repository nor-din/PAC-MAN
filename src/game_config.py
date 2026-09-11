"""Game constants for easy modification."""

from pathlib import Path
import json
from typing import Union
from pydantic import BaseModel, Field, field_validator, ValidationError

class ConfigError(Exception):
    """Exception raised for errors during configuration parsing."""
    def __init__(self, message: str, key: str = None, value: any = None):
        self.key = key
        self.value = value
        self.message = message
        
        detail = message
        if key is not None:
            detail = f"Configuration Error -> Key: '{key}', Value: '{value}' | Reason: {message}"
            
        super().__init__(detail)


class GameConfig(BaseModel):
    # --- User Modifiable Settings ---
    lives: int = Field(default=3, gt=0, lt=99)
    points_per_pacgum: int = Field(default=10, gt=0, le=1000000)
    points_per_super_pacgum: int = Field(default=50, gt=0, le=1000000)
    points_per_ghost: int = Field(default=200, gt=0, le=1000000)
    seed: Union[int, float, str, None] = Field(default=None)
    level_max_time: int = Field(default=90, gt=0, le=3600)

    # --- Internal / Dev-Only Settings ---
    highscore_filename: str = Field(default="highscore.json")
    ghost_respawn_ms: int = Field(default=8000, gt=0, le=3600000)
    super_pacgum_duration_ms: int = Field(default=7000, gt=0, le=3600000)
    scatter_duration_ms: int = Field(default=7000, gt=0, le=3600000)
    chase_duration_ms: int = Field(default=20000, gt=0, le=3600000)
    fps: int = Field(default=60, gt=0)
    player_speed_ticks: int = Field(default=10, gt=0)
    ghost_speed_ticks: int = Field(default=30, gt=0)
    player_default_move: int = Field(default=1, gt=0)
    player_cheat_move: int = Field(default=2, gt=0)


def remove_comments(lines):
    clean_lines = []
    for line in lines:
        clean_lines.append(line.partition('#')[0])
    return "\n".join(clean_lines)


def parse_config(filename: str) -> GameConfig:
    allowed_user_keys = {
        "lives",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "seed",
        "level_max_time"
    }

    valid_overrides = {}

    try:
        with open(filename, 'r') as config_file:
            cleaned_file = remove_comments(config_file.readlines())
            user_config = json.loads(cleaned_file)

        for k, v in user_config.items():
            if k in allowed_user_keys:
                try:
                    # Test if this single key-value pair is valid
                    GameConfig(**{k: v})
                    valid_overrides[k] = v
                except ValidationError as e:
                    # Use our ConfigError to format the error, but don't raise it
                    error_msg = e.errors()[0].get('msg', 'Validation failed')
                    err = ConfigError(message=error_msg, key=k, value=v)
                    print(f"Warning: Silently ignoring bad parameter. {err}")
                    pass

    except FileNotFoundError:
        print(f"Warning: Config file '{filename}' not found. Using defaults.")
    except PermissionError:
        print(f"Warning: Permission denied for config file '{filename}'. Using defaults.")
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON in config file '{filename}': {e}. Using defaults.")
    except Exception as e:
        print(f"Warning: Error reading config file '{filename}': {e}. Using defaults.")

    # Return the final config object containing defaults + valid user overrides
    return GameConfig(**valid_overrides)
