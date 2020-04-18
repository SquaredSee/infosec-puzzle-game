"""engine.py: Basic game primitives and global constants"""

import sys
from enum import Enum
from os.path import join
from types import SimpleNamespace

from pygame import Surface, display
from pygame.color import Color
from pygame.key import get_pressed
from pygame.sprite import Sprite, Group as SpriteGroup

# Target FPS for clock
FPS = 60

# Initial screen size constants
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
    NAVY = Color('#001f3f'),
    BLUE = Color('#0074D9'),
    AQUA = Color('#7FDBFF'),
    TEAL = Color('#39CCCC'),
    OLIVE = Color('#3D9970'),
    GREEN = Color('#2ECC40'),
    LIME = Color('#01FF70'),
    YELLOW = Color('#FFDC00'),
    ORANGE = Color('#FF851B'),
    RED = Color('#FF4136'),
    MAROON = Color('#85144b'),
    FUCHSIA = Color('#F012BE'),
    PURPLE = Color('#B10DC9'),
    BLACK = Color('#111111'),
    GRAY = Color('#AAAAAA'),
    SILVER = Color('#DDDDDD'),
    WHITE = Color('#FFFFFF'),
    TRANSPARENT = Color('#000000')
)

class Level(Enum):
    START = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    END = 5

# Game state, maintains progress between teleports and can be saved
State = SimpleNamespace(
    windowsize = SCREEN_SIZE,
    level = Level.START,
    teleport = None,  # value specifying stage to teleport to, or None
    player = None,
    keys = [False, False, False, False]
)


class Entity(Sprite):
    """Base class for all entities"""

    # Keep a group of all entities for the purpose of updating and drawing
    group = SpriteGroup()

    def __init__(self, size=(1, 1), gridpos=(0,0), color=COLOR.TRANSPARENT):
        Sprite.__init__(self)

        # Radius attribute for collision detection, circle centered on pos
        # self.radius = size[0] / 2

        self.gridsize = size

        self.size = size
        self.pos = gridpos
        self.gridpos = gridpos
        self.color = color
        self.resize = False

        self.image = Surface(size).convert()
        self.image.set_colorkey(COLOR.TRANSPARENT)  # set black as transparency color
        self.image.fill(color)

        self.rect = self.image.get_rect(topleft=self.pos)

        Entity.group.add(self)

    def update(self):
        """Called every tick to update the state of the entity"""
        Sprite.update(self)
        self.rect.topleft = self.pos
        if self.resize:
            self.resize = False
            self.image = Surface(self.size).convert()
            self.image.fill(self.color)
            self.rect = self.image.get_rect(topleft=self.pos)


class Wall(Entity):
    def __init__(self, gridpos=(0,0), color=COLOR.BLACK):
        Entity.__init__(self, gridpos=gridpos, color=color)


class Teleporter(Entity):
    def __init__(self, gridpos=(0,0), color=COLOR.BLUE, destination=Level.START):
        Entity.__init__(self, gridpos=gridpos, color=color)
        self.destination = destination


class Key(Entity):
    def __init__(self, val=0, gridpos=(0,0), color=COLOR.YELLOW):
        Entity.__init__(self, gridpos=gridpos, color=color)

        self.visible = True
        self.val = val

    def pick_up(self):
        print('test')
        State.keys[self.val] = True

    def update(self):
        Entity.update(self)
        if State.keys[self.val] and self.visible:
            self.visible = False
            self.image.set_alpha(0)


class Door(Entity):
    def __init__(self, val=0, gridpos=(0,0), color=COLOR.BLACK):
        Entity.__init__(self, gridpos=gridpos, color=color)

        self.val = val
        self.locked = True
        self.visible = True

    def update(self):
        Entity.update(self)
        if State.keys[self.val] and self.locked:
            self.locked = False
        elif not self.locked and self.visible:
            self.image.set_alpha(0)
            self.visible = False


class Board(Sprite):
    """
    Game board that handles drawing entities and tiles. Base class for all levels.
    """

    def __init__(self, gridsize=20, color=COLOR.GRAY):
        Sprite.__init__(self)

        # Radius attribute for collision detection, circle centered on pos
        # self.radius = size[0] / 2

        # self.state = state
        self.size = State.windowsize
        self.gridsize = gridsize
        self.color = color
        self.resize = True

        self.image = Surface(self.size).convert()
        # self.image.set_colorkey(COLOR.TRANSPARENT)  # set black as transparency color
        self.image.fill(color)

        self.x_u = self.size[0] / gridsize
        self.y_u = self.size[1] / gridsize
        self.x_offset = 0
        self.y_offset = 0

        self.spawncoords = (0,0)

        # Generate game grid
        self.grid = []
        for _ in range(gridsize):
            col = [None for _ in range(gridsize)]
            self.grid.append(col)

    def calc_pos(self, gridpos):
        """Calculates the screen position based on the grid size and the given coordinates"""
        x,y = gridpos
        x = self.x_offset + self.x_u * x
        y = self.y_offset + self.y_u * y
        return x, y

    def calc_size(self, size):
        """Calculates entity and tile size based on the grid size and the given coordinates"""
        s = (self.x_u * size[0] + 1, self.y_u * size[1] + 1)
        return s

    def place_player(self, gridpos=(0,0)):
        """Places the player stored in the State on the correct space on the grid"""
        x,y = gridpos
        if x < 0 or x > self.gridsize-1 or y < 0 or y > self.gridsize-1:
            # Restrict movement to within the grid
            return
        tile = self.grid[x][y]
        if tile:
            if type(tile) == Wall:
                # Don't move if the square is a wall
                return
            elif type(tile) == Teleporter:
                State.teleport = tile.destination
                return
            elif type(tile) == Key:
                tile.pick_up()
            elif type(tile) == Door and tile.locked:
                # Door is locked, don't move
                return
        old_x,old_y = State.player.gridpos
        State.player.gridpos = gridpos
        State.player.pos = self.calc_pos(gridpos)
        self.grid[old_x][old_y] = None
        self.grid[x][y] = State.player

    def spawn_player(self):
        self.place_player(self.spawncoords)

    def resize_board(self):
        """Re-calculate the sizes and positions of the entities on window resize"""
        if self.resize:
            self.resize = False

            w, h = State.windowsize
            self.size = (w, h)

            self.x_offset = (w - h) / 2
            if self.x_offset < 0:
                # Y direction longer than X, pad top and use width for sizing
                self.x_u = w / self.gridsize
                self.y_u = w / self.gridsize
                self.x_offset = 0
                self.y_offset = (h - w) / 2
            else:
                # X direction longer than Y, pad left and use height for sizing
                self.x_u = h / self.gridsize
                self.y_u = h / self.gridsize
                self.y_offset = 0

            self.image = Surface((w, h)).convert()
            self.image.fill(COLOR.GRAY)

            # Re-calculate all tile sizes and positions
            for col in self.grid:
                for i in range(len(col)):
                    if col[i]:
                        col[i].resize = True
                        col[i].pos = self.calc_pos(col[i].gridpos)
                        col[i].size = self.calc_size(col[i].gridsize)

    def update(self):
        """Called every tick to update the state of the board"""
        Sprite.update(self)
        self.resize_board()

    def kill(self):
        for col in self.grid:
            for i in range(len(col)):
                if col[i]:
                    col[i].kill()
        Sprite.kill(self)


def generate_grid(board, wall_color=COLOR.BLACK, tele_color=COLOR.TEAL, door_color=COLOR.GREEN, key_color=COLOR.YELLOW):
    l = len(board)
    grid = [[None for _ in range(l)] for _ in range(l)]
    for y in range(l):
        for x in range(l):
            val = board[y][x]
            if val == '':
                continue
            elif val == 'w':
                grid[x][y] = Wall(
                    gridpos=(x,y),
                    color=wall_color
                )
            elif 't' in val:
                d = int(val[1])
                dest = Level(d)
                grid[x][y] = Teleporter(
                    gridpos=(x,y),
                    color=tele_color,
                    destination=dest
                )
            elif 'd' in val:
                v = int(val[1])
                grid[x][y] = Door(
                    val=v-1,
                    gridpos=(x,y),
                    color=door_color
                )
            elif 'k' in val:
                v = int(val[1])
                grid[x][y] = Key(
                    val=v-1,
                    gridpos=(x,y),
                    color=key_color
                )
    return grid
