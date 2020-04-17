"""game.py: Main game loop and event handling"""

from pygame import Surface, display, init
from pygame.event import get as get_events
from pygame.locals import RESIZABLE, VIDEORESIZE, QUIT, K_RETURN
from pygame.time import Clock

from engine import Entity, State, Level, COLOR, FPS, FONT_PATH, FONT_SIZE
from levels import LevelStart, LevelOne
from player import Player


def spawn_player(board):
    if State.player:
        State.player.kill()
    State.player = Player()
    board.place_player()


def main():
    init()

    clock = Clock()

    screen = display.set_mode(State.windowsize, RESIZABLE)
    display.set_caption('HACK!')

    board = LevelStart()
    spawn_player(board)

    while True:
        for event in get_events():
            if event.type == QUIT:
                raise SystemExit('Thanks for playing!')
            if event.type == VIDEORESIZE:
                # Reset screen surface and set resize flag on board
                size = (event.w, event.h)
                screen = display.set_mode(size, RESIZABLE)
                State.windowsize = size
                board.resize = True

        if State.teleport:
            board.kill()
            State.level = State.teleport
            if State.teleport == Level.START:
                board = LevelStart()
            elif State.teleport == Level.ONE:
                board = LevelOne()
            spawn_player(board)
            State.teleport = None

        # Update all entities and draw them
        screen.blit(board.image, (0, 0))
        board.update()
        Entity.group.update()
        Entity.group.draw(screen)

        # Display what has been drawn
        display.update()

        # Advance the clock
        clock.tick(FPS)


if __name__ == '__main__':
    main()
