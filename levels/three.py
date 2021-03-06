"""three.py"""

from engine import Board, generate_grid

BOARD = [
    ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
    ['w', '', '', '', 'w', '', '', '', '', '', '', '', '', '', '', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', '', '', '', '', '', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', 'w', 'w', 'w', 'w', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', 'w', '', '', '', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', 'w', '', 'w', '', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', 'w', 'w', 'w', '', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', 'k4', 'w', 'w', '', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', '', 't0', 'w', 'w', '', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', 'w', 'w', 'w', 'w', '', '', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', '', '', '', '', '', '', 'w', 'w', '', 'w', '', 'w'],
    ['w', '', 'w', '', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', '', '', 'w', '', 'w'],
    ['w', '', 'w', '', '', '', '', '', '', '', '', '', '', 'w', 'w', '', 'w'],
    ['w', '', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 't0', '', 'w'],
    ['w', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'w'],
    ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
]


class LevelThree(Board):
    """LevelThree"""

    def __init__(self):
        Board.__init__(self, gridsize=17)

        self.grid = generate_grid(BOARD)
        self.spawncoords = (15,15)
