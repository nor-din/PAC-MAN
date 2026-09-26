"""Module for managing developer cheat codes and game modifications."""


class Cheat:
    """Manages developer cheat codes.

    Attributes:
        frezz: Freezes ghosts.
        invincible: Player cannot be killed.
        speed: Player moves faster.
        skip_level: Skip to the next level.
    """

    def __init__(self) -> None:
        """Initialize all cheats to False.

        Returns:
            None.
        """
        self.frezz = False
        self.invincible = False
        self.speed = False
        self.skip_level = False
