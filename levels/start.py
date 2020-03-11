"""start.py: Starting level, contains teleports to all other levels."""

from engine import Board


class LevelStart(Board):
    """
    Main warp stage, player spawns and can teleport to any other stage.
    End doors are unlocked by collecting items from each stage.
    """

    def __init__(self):
        Board.__init__(self)
