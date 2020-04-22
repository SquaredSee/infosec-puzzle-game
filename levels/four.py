"""four.py"""

from engine import Board, generate_grid

BOARD = [
    ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
    ['w', '', 'w', '', '', '', 'w', '', '', '', 'w'],
    ['w', '', '', '', 'w', '', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', 'w', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', '', '', '', '', 'w', 'k5', 'w'],
    ['w', '', 'w', 'w', 'w', '', 'w', 'w', 'w', 't0', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', '', 'w', 'w'],
    ['w', '', '', '', 'w', '', 'w', 'w', '', 'w', 'w'],
    ['w', 'p', 'w', '', '', '', '', '', '', '', 'w'],
    ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
]


class LevelFour(Board):
    """LevelFour"""

    def __init__(self):
        Board.__init__(self, gridsize=11)

        self.grid = generate_grid(BOARD)
        self.spawncoords = (1, 9)
