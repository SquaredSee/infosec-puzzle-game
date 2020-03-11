"""tiles.py: Definitions for all game board tiles"""

from engine import Entity


class Wall(Entity):
    """Wall tile, restricts player movement"""
    pass


class Door(Entity):
    """Door tile, can be controlled by a button"""
    pass


class Button(Entity):
    """Controls entities in the level"""
    pass


class Teleporter(Entity):
    """Transports the player to a different level"""
    pass
