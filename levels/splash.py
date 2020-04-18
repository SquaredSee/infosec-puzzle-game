"""splash.py"""

from pygame.image import load

from engine import Board, State, SPLASH


class SplashScreen(Board):
    """Splash screen"""

    def __init__(self):
        Board.__init__(self)
        self.splash = load(SPLASH)

    def update(self):
        Board.update(self)
        self.image = self.splash
