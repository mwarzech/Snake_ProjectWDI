import pygame, sys
from src.matrix import Matrix
from src.menu import Menu
from enum import Enum


class States(Enum):
    MENU = 1
    GAME = 2
    GAME_OVER = 3


class Game(object):
    def __init__(self):
        # Initialization
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.plane = Matrix(self, States)
        self.menu = Menu(self, States)
        self.current_state = States.MENU

        # Config
        self.tps_max = 5

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.mixer.Channel(0).stop()
                    self.current_state = States.MENU

            # Ticking
            self.tps_delta += self.tps_clock.tick()/1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.tps_delta -= 1 / self.tps_max

            # Drawing
            self.screen.fill((87, 189, 134))
            self.draw()
            pygame.display.flip()

    def tick(self):
        if self.current_state == States.GAME:
            self.plane.tick()

    def draw(self):
        if self.current_state == States.GAME or self.current_state == States.GAME_OVER:
            self.plane.draw()
        if self.current_state == States.MENU:
            self.menu.draw()
        if self.current_state == States.GAME_OVER:
            self.plane.game_over_draw()


if __name__ == "__main__":
    Game()
