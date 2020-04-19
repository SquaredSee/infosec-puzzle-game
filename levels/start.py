"""start.py: Starting level,contains teleports to all other levels."""

from engine import Board, generate_grid

BOARD = [
    ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','w','t5','w','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','w','d6','w','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','w','d5','w','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','w','d4','w','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','w','d3','w','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','w','d2','w','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','','','','','','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','','','','','','w','w','w','w','w','w'],
    ['w','w','w','w','t3','d3','','','','','','d4','t4','w','w','w','w'],
    ['w','w','w','w','w','w','','','','','','w','w','w','w','w','w'],
    ['w','w','w','w','t1','d1','','','','','','d2','t2','w','w','w','w'],
    ['w','w','w','w','w','w','','','k1','','','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','','','','','','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','','','','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','w','p','w','w','w','w','w','w','w','w'],
    ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w']
]


class LevelStart(Board):
    """
    Main warp stage, player spawns and can teleport to any other stage.
    End doors are unlocked by collecting items from each stage.
    """

    def __init__(self):
        Board.__init__(self, gridsize=17)

        self.spawncoords = (8, 15)

        self.grid = generate_grid(BOARD)
