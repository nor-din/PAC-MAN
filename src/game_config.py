"""Module for defining and parsing JSON configuration with fallback logic."""
import json
import sys
from typing import Union, Any
from pydantic import BaseModel, Field, ValidationError


class GameConfig(BaseModel):
    """Pydantic model for validating the JSON configuration file.

    Contains fields and constraints for level settings, points, and durations.
    """

    lives: int = Field(default=3, gt=0, lt=100)
    points_per_pacgum: int = Field(default=10, gt=0, le=1000)
    points_per_super_pacgum: int = Field(default=50, gt=0, le=5000)
    points_per_ghost: int = Field(default=200, gt=0, le=20000)
    seed: Union[int, float, str, None] = Field(default=None)
    level_max_time: int = Field(default=90, gt=0, le=3600)
    highscore_filename: str = Field(default='highscore.json')
    ghost_respawn_ms: int = Field(default=8000, gt=0, le=3600000)
    super_pacgum_duration_ms: int = Field(default=7000, gt=0, le=3600000)
    scatter_duration_ms: int = Field(default=7000, gt=0, le=3600000)
    chase_duration_ms: int = Field(default=20000, gt=0, le=3600000)
    player_speed_ticks: int = Field(default=12, gt=0)
    ghost_speed_ticks: int = Field(default=30, gt=0)
    player_default_move: int = Field(default=1, gt=0)
    player_cheat_move: int = Field(default=2, gt=0)

    def get_maze_seed(self, level: int) -> int:
        """Generate a positive integer seed for the maze generator.

        The first level uses a deterministic seed (either based on the provided
        config seed or a default one) so that it is always the same.
        Subsequent levels return 0 to trigger random generation.

        Args:
            level: The current game level.

        Returns:
            A positive integer suitable for the MazeGenerator, or 0 for random.
        """
        if level > 1:
            return 0

        if self.seed is None:
            seed_str = "default_seed"
        else:
            seed_str = f"{self.seed}_{level}"

        return sum(ord(c) for c in seed_str)

    @staticmethod
    def remove_comments(lines: list[str]) -> str:
        """Remove '#' comments from a JSON string.

        Args:
            lines: A list of string lines from the config file.

        Returns:
            A single sanitized JSON string.
        """
        clean_lines = []
        for line in lines:
            clean_lines.append(line.split('#')[0])
        return '\n'.join(clean_lines)

    @staticmethod
    def detect_duplicate_keys(
            ordered_pairs: 'list[tuple[str, Any]]') -> 'dict[str, Any]':
        """Object pairs hook to detect duplicate keys during JSON parsing.

        Args:
            ordered_pairs: A list of key-value pairs parsed from JSON.

        Returns:
            A dictionary constructed from the pairs with duplicates ignored.
        """
        d: 'dict[str, Any]' = {}

        for k, v in ordered_pairs:
            if k in d:
                print(
                    f"Warning: Duplicated key '{k}'. Ignoring second value.",
                    file=sys.stderr)
            else:
                d[k] = v

        return d

    @classmethod
    def parse_config(cls, filename: str) -> "GameConfig":
        """Load, sanitizes, and validates the config file.

        Args:
            filename: Path to the JSON configuration file.

        Returns:
            A validated GameConfig instance with safe fallbacks applied.

        """
        allowed_user_keys = {
            'lives',
            'points_per_pacgum',
            'points_per_super_pacgum',
            'points_per_ghost',
            'seed',
            'level_max_time'
        }

        valid_overrides = {}

        try:
            with open(filename, 'r') as config_file:
                cleaned_file = cls.remove_comments(config_file.readlines())
                user_config = json.loads(
                    cleaned_file, object_pairs_hook=cls.detect_duplicate_keys)
            for (k, v) in user_config.items():
                if k in allowed_user_keys:
                    try:
                        cls.model_validate({k: v})
                        valid_overrides[k] = v
                    except ValidationError as e:
                        error_msg = ", ".join(err['msg'] for err in e.errors())
                        print(
                            f"Invalid '{v}' for '{k}'. {error_msg}.",
                            file=sys.stderr)
                else:
                    print(
                        f"Warning: Unknown key '{k}'. Ignoring.",
                        file=sys.stderr)
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

        return cls(**valid_overrides)
