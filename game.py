"""game.py: Main game loop and event handling"""

from pygame import Surface, display, init
from pygame.event import get as get_events
from pygame.locals import RESIZABLE, VIDEORESIZE, QUIT, K_RETURN
from pygame.time import Clock

from engine import Board, Entity, State, COLOR, FPS, FONT_PATH, FONT_SIZE


def main():
    init()

    clock = Clock()

    screen = display.set_mode(State['windowsize'], RESIZABLE)
    display.set_caption('HACK!')

    board = Board()

    while True:
        for event in get_events():
            if event.type == QUIT:
                raise SystemExit('Thanks for playing!')
            if event.type == VIDEORESIZE:
                # Reset screen surface and set resize flag on board
                size = (event.w, event.h)
                screen = display.set_mode(size, RESIZABLE)
                State['windowsize'] = size
                board.resize = True

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
