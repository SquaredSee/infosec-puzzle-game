"""player.py: Player and related Entities"""

from pygame.draw import lines as draw_lines
from pygame.key import get_pressed
from pygame.math import Vector2 as Vector
from pygame.sprite import Group as SpriteGroup

from engine import Entity, State, COLOR

class Player(Entity):
    """Entity for the player"""

    def __init__(self, gridpos=(0,0)):
        Entity.__init__(self, (1,1), gridpos, color=COLOR.RED)

        # Draws an arrow facing in the direction of angle to serve as the ship
        # size = self.image.get_size()
        # arrow_points = [
        #     (0, size[1] - 1),  # bottom left
        #     ((size[0] - 1) / 2, 0),  # top middle
        #     (size[0] - 1, size[1] - 1)  # bottom right
        # ]
        # draw_lines(self.image, COLOR.WHITE, False, arrow_points, 2)

    # def kill(self):
    #     Entity.kill(self)

    # def update(self):
    #     Entity.update(self)
