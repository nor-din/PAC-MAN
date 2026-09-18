from __future__ import annotations
'Game constants for easy modification.'
import json
import sys
from typing import Union
from pydantic import BaseModel, Field, ValidationError


class GameConfig(BaseModel):
    """Pydantic model for validating the JSON configuration file.

    Contains fields and constraints for level settings, points, and durations.
    """

    lives: int = Field(default=3, gt=0, lt=99)
    points_per_pacgum: int = Field(default=10, gt=0, le=1000000)
    points_per_super_pacgum: int = Field(default=50, gt=0, le=1000000)
    points_per_ghost: int = Field(default=200, gt=0, le=1000000)
    seed: Union[int, float, str, None] = Field(default=None)
    level_max_time: int = Field(default=90, gt=0, le=3600)
    highscore_filename: str = Field(default='highscore.json')
    ghost_respawn_ms: int = Field(default=8000, gt=0, le=3600000)
    super_pacgum_duration_ms: int = Field(default=7000, gt=0, le=3600000)
    scatter_duration_ms: int = Field(default=7000, gt=0, le=3600000)
    chase_duration_ms: int = Field(default=20000, gt=0, le=3600000)
    fps: int = Field(default=60, gt=0)
    player_speed_ticks: int = Field(default=12, gt=0)
    ghost_speed_ticks: int = Field(default=30, gt=0)
    player_default_move: int = Field(default=1, gt=0)
    player_cheat_move: int = Field(default=2, gt=0)


def remove_comments(lines: list[str]) -> str:
    """Removes '#' comments from a JSON string.

    Args:
        lines: A list of string lines from the config file.

    Returns:
        A single sanitized JSON string.
    """
    clean_lines = []
    for line in lines:
        clean_lines.append(line.split('#')[0])
    return '\n'.join(clean_lines)


def parse_config(filename: str) -> GameConfig:
    """Loads, sanitizes, and validates the config file.

    Args:
        filename: Path to the JSON configuration file.

    Returns:
        A validated GameConfig instance with safe fallbacks applied.

    Raises:
        SystemExit: If configuration fails completely.
    """
    allowed_user_keys = {
        'lives',
        'points_per_pacgum',
        'points_per_super_pacgum',
        'points_per_ghost',
        'seed',
        'level_max_time'}
    valid_overrides = {}
    try:
        with open(filename, 'r') as config_file:
            cleaned_file = remove_comments(config_file.readlines())
            user_config = json.loads(cleaned_file)
        for (k, v) in user_config.items():
            if k in allowed_user_keys:
                try:
                    GameConfig.model_validate({k: v})
                    valid_overrides[k] = v
                except ValidationError as e:
                    error_msg = e.errors()[0].get('msg', 'Validation failed')
                    print(
                        f"Invalid '{v}' for '{k}'. {error_msg}.",
                        file=sys.stderr)
            else:
                f"Warning: Unknown key '{k}'. Ignoring.",
    except FileNotFoundError:
        print(
            f"Warning: Config file '{filename}' not found.",
            file=sys.stderr)
    except PermissionError:
        print(
            f"Warning: Permission denied '{filename}'. Using defaults.",
            file=sys.stderr)
    except json.JSONDecodeError as e:
        print(
            f"Warning: Invalid JSON in '{filename}': {e}.",
            file=sys.stderr)
    except Exception as e:
        print(
            f"Warning: Error reading '{filename}': {e}. Using defaults.",
            file=sys.stderr)
    return GameConfig(**valid_overrides)
