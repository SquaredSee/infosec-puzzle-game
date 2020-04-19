"""end.py"""

from pygame.image import load

from engine import Board, State, END


class EndScreen(Board):
    """End screen"""

    def __init__(self):
        Board.__init__(self)
        self.end = load(END)

    def update(self):
        Board.update(self)
        self.image = self.end
