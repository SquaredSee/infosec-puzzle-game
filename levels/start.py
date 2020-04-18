"""start.py: Starting level, contains teleports to all other levels."""

from engine import COLOR, Level, Board, State, Wall, Teleporter


class LevelStart(Board):
    """
    Main warp stage, player spawns and can teleport to any other stage.
    End doors are unlocked by collecting items from each stage.
    """

    def __init__(self):
        Board.__init__(self)

        self.grid[3][3] = Teleporter(
            gridpos=(3,3),
            color=COLOR.TEAL,
            destination=Level.ONE
        )

        # Add entity for testing
        self.grid[9][9] = Wall(
            gridpos=(9, 9),
            color=COLOR.RED
        )
        self.grid[10][10] = Wall(
            gridpos=(10, 10),
            color=COLOR.BLUE
        )
        self.grid[19][19] = Wall(
            gridpos=(19, 19),
            color=COLOR.GREEN
        )
