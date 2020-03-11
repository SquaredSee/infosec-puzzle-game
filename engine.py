"""engine.py: Basic game primitives and global constants"""

import sys
from os.path import join
from types import SimpleNamespace

from pygame import Surface, display
from pygame.color import Color
from pygame.sprite import Sprite, Group as SpriteGroup

FPS = 60
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    DATA_PATH = join(sys._MEIPASS, 'data')
except Exception:
    DATA_PATH = join('.', 'data')

FONT_PATH = join(DATA_PATH, 'PressStart2P-Regular.ttf')
FONT_SIZE = 36

# Use a SimpleNamespace to allow for COLOR.NAME accessing
COLOR = SimpleNamespace(
    NAVY=Color('#001f3f'),
    BLUE=Color('#0074D9'),
    AQUA=Color('#7FDBFF'),
    TEAL=Color('#39CCCC'),
    OLIVE=Color('#3D9970'),
    GREEN=Color('#2ECC40'),
    LIME=Color('#01FF70'),
    YELLOW=Color('#FFDC00'),
    ORANGE=Color('#FF851B'),
    RED=Color('#FF4136'),
    MAROON=Color('#85144b'),
    FUCHSIA=Color('#F012BE'),
    PURPLE=Color('#B10DC9'),
    BLACK=Color('#111111'),
    GRAY=Color('#AAAAAA'),
    SILVER=Color('#DDDDDD'),
    WHITE=Color('#FFFFFF'),
    TRANSPARENT=Color('#000000')
)


class Entity(Sprite):
    """Base class for all entities"""

    # Keep a group of all entities for the purpose of updating and drawing
    group = SpriteGroup()

    def __init__(self, size=(1, 1), pos=(0, 0), gridpos=(0,0), color=COLOR.TRANSPARENT):
        Sprite.__init__(self)

        # Radius attribute for collision detection, circle centered on pos
        # self.radius = size[0] / 2

        self.size = size
        self.pos = pos
        self.gridpos = gridpos
        self.color = color
        self.resize = False

        self.image = Surface(size).convert()
        self.image.set_colorkey(COLOR.TRANSPARENT)  # set black as transparency color
        self.image.fill(color)

        self.rect = self.image.get_rect(topleft=pos)

        Entity.group.add(self)

    def update(self):
        """Called every tick to update the state of the entity"""
        if self.resize:
            self.resize = False
            self.image = Surface(self.size).convert()
            self.image.fill(self.color)
            self.rect = self.image.get_rect(topleft=self.pos)


class Board(Sprite):
    """Game board that handles drawing entities and tiles. Base class for all levels."""

    def __init__(self, gridsize=(20,20), color=COLOR.GRAY):
        Sprite.__init__(self)

        # Radius attribute for collision detection, circle centered on pos
        # self.radius = size[0] / 2

        self.size = SCREEN_SIZE
        self.gridsize = gridsize
        self.color = color
        self.resize = False

        self.image = Surface(SCREEN_SIZE).convert()
        # self.image.set_colorkey(COLOR.TRANSPARENT)  # set black as transparency color
        self.image.fill(color)

        self.x_u = SCREEN_HEIGHT / gridsize[0]
        self.y_u = SCREEN_HEIGHT / gridsize[1]
        self.x_offset = 0
        self.y_offset = 0

        # Generate game grid
        self.grid = []
        for _ in range(gridsize[0]):
            col = [None for _ in range(gridsize[1])]
            self.grid.append(col)

        # Add entity for testing
        self.grid[4][4] = Entity(
            self.calc_size((1, 1)),
            self.calc_pos(4, 4),
            (4, 4),
            COLOR.RED
        )

    def calc_pos(self, x, y):
        """Calculates the screen position based on the grid size and the given coordinates"""
        x = self.x_offset + self.x_u * x
        y = self.y_offset + self.y_u * y
        return x, y

    def calc_size(self, size):
        """Calculates entity and tile size based on the grid size and the given coordinates"""
        size = (self.x_u * size[0], self.y_u * size[1])
        return size

    def update(self):
        """Called every tick to update the state of the board"""

        if self.resize:
            self.resize = False

            w, h = display.get_surface().get_size()
            self.size = (w, h)

            self.x_offset = (w - h) / 2
            if self.x_offset < 0:
                # Y direction longer than X, pad top and use width for sizing
                self.x_u = w / self.gridsize[0]
                self.y_u = w / self.gridsize[1]
                self.x_offset = 0
                self.y_offset = (h - w) / 2
            else:
                # X direction longer than Y, pad left and use height for sizing
                self.x_u = h / self.gridsize[0]
                self.y_u = h / self.gridsize[1]
                self.y_offset = 0

            self.image = Surface((w, h)).convert()
            self.image.fill(COLOR.GRAY)

            # Re-calculate all tile sizes and positions
            for x, col in enumerate(self.grid):
                for y in range(len(col)):
                    if col[y]:
                        col[y].resize = True
                        col[y].pos = self.calc_pos(x, y)
                        col[y].size = self.calc_size((1, 1))
