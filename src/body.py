import pygame
from pygame.math import Vector2


class Body(object):
    def __init__(self, game, index, pos, dir, next_dir):
        self.game = game
        self.index = index

        self.pos = pos
        self.last_pos = pos
        self.dir = dir
        self.next_dir = next_dir
        if dir==0:
            self.image = pygame.image.load("Data/snakeEndUp.png")
        elif dir == 1:
            self.image = pygame.image.load("Data/snakeEndRight.png")
        elif dir == 2:
            self.image = pygame.image.load("Data/snakeEndDown.png")
        elif dir == 3:
            self.image = pygame.image.load("Data/snakeEndLeft.png")
        self.color = (0, 150, 20)
        #self.reloadImage()

    def reloadImage(self,end=False):
        if(self.next_dir==0):
            if(end):
                self.image = pygame.image.load("Data/snakeEndUp.png")
            else:
                if(self.dir==0 or self.dir==2):
                    self.image = pygame.image.load("Data/snakeBodyVertical.png")
                elif(self.dir==1):
                    self.image = pygame.image.load("Data/snakeBodyTopAndLeft.png")
                elif (self.dir == 3):
                    self.image = pygame.image.load("Data/snakeBodyTopAndRight.png")
        elif(self.next_dir==1):
            if (end):
                self.image = pygame.image.load("Data/snakeEndRight.png")
            else:
                if (self.dir == 1 or self.dir == 3):
                    self.image = pygame.image.load("Data/snakeBodyHorizontal.png")
                elif (self.dir == 0):
                    self.image = pygame.image.load("Data/snakeBodyBottomAndRight.png")
                elif (self.dir == 2):
                    self.image = pygame.image.load("Data/snakeBodyTopAndRight.png")
        elif (self.next_dir== 2):
            if (end):
                self.image = pygame.image.load("Data/snakeEndDown.png")
            else:
                if (self.dir == 0 or self.dir == 2):
                    self.image = pygame.image.load("Data/snakeBodyVertical.png")
                elif (self.dir == 1):
                    self.image = pygame.image.load("Data/snakeBodyBottomAndLeft.png")
                elif (self.dir == 3):
                    self.image = pygame.image.load("Data/snakeBodyBottomAndRight.png")
        elif (self.next_dir== 3):
            if (end):
                self.image = pygame.image.load("Data/snakeEndLeft.png")
            else:
                if (self.dir == 1 or self.dir == 3):
                    self.image = pygame.image.load("Data/snakeBodyHorizontal.png")
                elif (self.dir == 0):
                    self.image = pygame.image.load("Data/snakeBodyBottomAndLeft.png")
                elif (self.dir == 2):
                    self.image = pygame.image.load("Data/snakeBodyTopAndLeft.png")
        self.image = pygame.transform.scale(self.image,(int(self.game.plane.field_size.x), int(self.game.plane.field_size.y)))

    def will_eat(self):
        return (self.game.plane.head.pos.x+self.game.plane.head.dir_vector.x == self.game.plane.apple_pos.x) and (self.game.plane.head.pos.y+self.game.plane.head.dir_vector.y == self.game.plane.apple_pos.y)

    def tick(self):
        # Moving
        self.last_pos = Vector2(self.pos.x, self.pos.y)
        if(self.index>1):
            self.dir = self.game.plane.sneak[self.index-1].dir
            self.next_dir = self.game.plane.sneak[self.index-2].dir
            self.pos = Vector2(self.game.plane.sneak[self.index-1].pos.x,self.game.plane.sneak[self.index-1].pos.y)
        elif (self.index > 0):
            self.dir = self.game.plane.sneak[self.index - 1].dir
            self.next_dir = self.game.plane.head.prev_dir
            self.pos = Vector2(self.game.plane.sneak[self.index - 1].pos.x, self.game.plane.sneak[self.index - 1].pos.y)
        else:
            self.dir = self.game.plane.head.prev_dir
            self.next_dir = self.game.plane.head.dir
            self.pos = Vector2(self.game.plane.head.pos.x, self.game.plane.head.pos.y)
        if(self.index==len(self.game.plane.sneak)-1) and self.will_eat() is False:
            self.reloadImage(True)
        else:
            self.reloadImage()

    def draw(self):
        self.image = pygame.transform.scale(self.image, (int(self.game.plane.field_size.x), int(self.game.plane.field_size.y)))
        real_pos_x = self.pos.x*self.game.plane.field_size.x + self.game.plane.draw_start_pos.x
        real_pos_y = self.pos.y*self.game.plane.field_size.y + self.game.plane.draw_start_pos.y
        rect = pygame.Rect(real_pos_x, real_pos_y, self.game.plane.field_size.x, self.game.plane.field_size.y)
        self.game.screen.blit(self.image, rect)
