import pygame
from pygame.math import Vector2
import shelve

class Head(object):
    def __init__(self, game, states):
        self.game = game
        self.States = states
        self.pos = Vector2(0, 0)
        self.last_pos = Vector2(self.pos.x,self.pos.y)
        self.dir = 1  # dir 0==(0,-1)up 1==(1,0)right 2==(0,1)down 3==(-1,0)left
        self.prev_dir = self.dir
        self.dir_vector = Vector2(0, 0)
        self.press_dir = 1
        self.color = (0, 200, 50)
        self.image = pygame.image.load("Data/snakeHeadRight.png")



    def reloadImage(self,eating=False,dead=False):
        if(self.dir==0):
            if eating:
                self.image = pygame.image.load("Data/snakeHeadEatUp.png")
            elif dead:
                self.image = pygame.image.load("Data/snakeHeadDeadUp.png")
            else:
                self.image = pygame.image.load("Data/snakeHeadUp.png")
        elif(self.dir==1):
            if (eating):
                self.image = pygame.image.load("Data/snakeHeadEatRight.png")
            elif dead:
                self.image = pygame.image.load("Data/snakeHeadDeadRight.png")
            else:
                self.image = pygame.image.load("Data/snakeHeadRight.png")
        elif (self.dir == 2):
            if (eating):
                self.image = pygame.image.load("Data/snakeHeadEatDown.png")
            elif dead:
                self.image = pygame.image.load("Data/snakeHeadDeadDown.png")
            else:
                self.image = pygame.image.load("Data/snakeHeadDown.png")
        elif (self.dir == 3):
            if (eating):
                self.image = pygame.image.load("Data/snakeHeadEatLeft.png")
            elif dead:
                self.image = pygame.image.load("Data/snakeHeadDeadLeft.png")
            else:
                self.image = pygame.image.load("Data/snakeHeadLeft.png")
        self.image = pygame.transform.scale(self.image,(int(self.game.plane.field_size.x), int(self.game.plane.field_size.y)))

    def set_dir(self):
        self.last_pos = Vector2(self.pos.x, self.pos.y)
        self.prev_dir = self.dir
        # Inputs
        press = pygame.key.get_pressed()
        if self.press_dir == 0 and self.dir != 2:
            self.dir = 0
        elif self.press_dir == 2 and self.dir != 0:
            self.dir = 2
        elif self.press_dir == 3 and self.dir != 1:
            self.dir = 3
        elif self.press_dir == 1 and self.dir != 3:
            self.dir = 1

        # Moving
        if self.dir == 0:
            self.dir_vector = Vector2(0, -1)
        elif self.dir == 1:
            self.dir_vector = Vector2(1, 0)
        elif self.dir == 2:
            self.dir_vector = Vector2(0, 1)
        elif self.dir == 3:
            self.dir_vector = Vector2(-1, 0)

    def tick(self):
        self.set_dir()
        self.pos += self.dir_vector

        if (self.game.plane.apple_pos.x == self.pos.x and self.game.plane.apple_pos.y == self.pos.y):
            self.reloadImage(True)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Data/eatingApple.wav'))
            self.game.plane.growing()
            self.game.plane.spawn_apple()
        else:
            self.reloadImage()

    def check_if_crash(self):
        if self.pos.x<0 or self.pos.x>self.game.plane.matrix_size.x-1 or self.pos.y<0 or self.pos.y > self.game.plane.matrix_size.y-1:
            self.game_over()
            return
        for i in range(len(self.game.plane.sneak)):
            if self.game.plane.sneak[i].pos.x == self.pos.x and self.game.plane.sneak[i].pos.y == self.pos.y:
                self.game_over()
                return

    def game_over(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Data/GameOver.mp3")
        pygame.mixer.music.play(0)
        self.reloadImage(False, True)
        self.game.current_state = self.States.GAME_OVER

    def draw(self):
        # Inputs
        press = pygame.key.get_pressed()
        if (press[pygame.K_w] or press[pygame.K_UP]) and self.dir != 2:
            self.press_dir = 0
        elif (press[pygame.K_s] or press[pygame.K_DOWN]) and self.dir != 0:
            self.press_dir = 2
        elif (press[pygame.K_a] or press[pygame.K_LEFT]) and self.dir != 1:
            self.press_dir = 3
        elif (press[pygame.K_d] or press[pygame.K_RIGHT]) and self.dir != 3:
            self.press_dir = 1
        self.image = pygame.transform.scale(self.image,(int(self.game.plane.field_size.x), int(self.game.plane.field_size.y)))
        real_pos_x = self.pos.x*self.game.plane.field_size.x+self.game.plane.draw_start_pos.x
        real_pos_y = self.pos.y*self.game.plane.field_size.y+self.game.plane.draw_start_pos.y
        rect = pygame.Rect(real_pos_x,real_pos_y,self.game.plane.field_size.x,self.game.plane.field_size.y)
        self.game.screen.blit(self.image, rect)
