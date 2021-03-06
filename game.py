"""game.py: Main game loop and event handling"""

from pygame import Surface, display, init, K_RETURN, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_z
from pygame.event import get as get_events
from pygame.locals import RESIZABLE, VIDEORESIZE, QUIT, KEYDOWN
from pygame.time import Clock

from engine import Entity, Player, State, Level, COLOR, FPS
from levels import (SplashScreen, LevelStart, LevelOne,
    LevelTwo, LevelThree, LevelFour, EndScreen)


def spawn_player(board):
    """Deletes the existing player object and spawns a new one on the given board"""
    if State.player:
        State.player.kill()
    if type(board) == EndScreen:
        return
    State.player = Player(board.spawncoords)
    board.spawn_player()


def main():
    """Main game loop and event handling"""
    init()

    clock = Clock()

    screen = display.set_mode(State.windowsize, RESIZABLE)
    display.set_caption('HACK_')

    board = SplashScreen()

    while True:
        for event in get_events():
            if event.type == QUIT:
                raise SystemExit('Thanks for playing!')
            elif event.type == VIDEORESIZE:
                # Reset screen surface and set resize flag on board
                size = (event.w, event.h)
                screen = display.set_mode(size, RESIZABLE)
                State.windowsize = size
                board.resize = True
            elif event.type == KEYDOWN:
                if event.key == K_RETURN :
                    if type(board) == SplashScreen:
                        State.teleport = Level.START
                    elif type(board) == EndScreen:
                        return
                    continue

                try:
                    x,y = State.player.gridpos
                except AttributeError:
                    # Player won't exist in some situations, so don't fail here
                    continue
                if event.key == K_UP:
                    y -= 1
                if event.key == K_DOWN:
                    y += 1
                if event.key == K_LEFT:
                    x -= 1
                if event.key == K_RIGHT:
                    x += 1
                board.place_player((x,y))

        if State.teleport:
            # Transport the player to a different level
            board.kill()
            State.level = State.teleport
            if State.teleport == Level.START:
                board = LevelStart()
            elif State.teleport == Level.ONE:
                board = LevelOne()
            elif State.teleport == Level.TWO:
                board = LevelTwo()
            elif State.teleport == Level.THREE:
                board = LevelThree()
            elif State.teleport == Level.FOUR:
                board = LevelFour()
            elif State.teleport == Level.END:
                board = EndScreen()
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
