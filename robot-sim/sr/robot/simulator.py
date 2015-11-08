from __future__ import division

import threading, time, pygame, sys

from arenas import PiratePlunderArena, CTFArena, LiamArena
from display import Display

DEFAULT_GAME = 'liam'

GAMES = {'pirate-plunder': PiratePlunderArena,
         'ctf': CTFArena, 'liam': LiamArena}
GAME_CODES = {'pirate-plunder':0, 'ctf':1, 'liam': 2}
GAME_CODE = GAME_CODES[DEFAULT_GAME]

class Simulator(object):
    def __init__(self, config={}, size=(8, 8), frames_per_second=30, foreground=False):
        try:
            game_name = config['game']
            del config['game']
        except KeyError:
            game_name = DEFAULT_GAME
        game = GAMES[game_name]
        self.GAME_CODE = GAME_CODES[game_name]
        self.arena = game(**config)
        
        self.display = Display(self.arena, self.GAME_CODE)

        self.foreground = foreground
        self.frames_per_second = frames_per_second

        if not self.foreground:
            self._loop_thread = threading.Thread(target=self._main_loop, args=(frames_per_second,))
            self._loop_thread.setDaemon(True)
            self._loop_thread.start()

    def run(self):
        if not self.foreground:
            raise RuntimeError('Simulator runs in the background. Try passing foreground=True')
        self._main_loop(self.frames_per_second)

    def set_robots(self, robots):
        self.robots = robots

    def _main_loop(self, frames_per_second):
        clock = pygame.time.Clock()

        while True:
            if any(event.type == pygame.QUIT
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                    for event in pygame.event.get()):
                break

            self.display.tick(1/frames_per_second)
            clock.tick(frames_per_second)
        
        for robot in self.robots:
            try:
                robot.raiseExc(KeyboardInterrupt)
            except threading.ThreadError:
                pass
        
        pygame.quit()
        sys.exit(0)
        
