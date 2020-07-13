import pygame
from pygame.math import Vector2
from src.head import Head
from src.body import Body
from random import randint
import shelve


class Matrix(object):
    def __init__(self, game, states):
        self.game = game
        self.game.tps_max = 5
        self.States = states
        self.border_color = (int(87*0.75), int(189*0.75), int(134*0.75))
        self.screen_size = self.game.screen.get_size()
        self.matrix_size = Vector2(20, 19)
        self.field_size = Vector2((self.screen_size[0]*32)//1280, (self.screen_size[1]*32)//720)
        self.draw_start_pos = Vector2(self.screen_size[0]/2.0-(self.matrix_size.x*self.field_size.x)/2.0, 80)

        # Apple config
        self.apple_pos = Vector2(randint(1, self.matrix_size.x-1), randint(1, self.matrix_size.y-1))
        self.apple_color = (250, 50, 50)
        self.apple_image = pygame.image.load("Data/apple2.png")
        self.apple_image = pygame.transform.scale(self.apple_image, (int(self.field_size.x), int(self.field_size.y)))

        self.background_image = pygame.image.load("Data/background.png")
        self.foreground_image = pygame.image.load("Data/foreground.png")
        self.background_size = 1
        self.background_image = pygame.transform.scale(self.background_image, (int(self.screen_size[0] * self.background_size), int(self.screen_size[1] * self.background_size)))
        self.foreground_image = pygame.transform.scale(self.foreground_image, (int(self.screen_size[0] * self.background_size), int(self.screen_size[1] * self.background_size)))

        self.head = Head(game, states)
        self.sneak = [Body(self.game,0,self.head.last_pos,1,1)]

        self.points = len(self.sneak) - 1

        # Music config
        pygame.mixer.music.load("Data/Popcorn.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.Channel(0).stop()


    def growing(self):
        self.game.tps_max += 0.2
        if self.game.tps_max > 30:
            self.game.tps_max = 30
        index = len(self.sneak)
        if index>1:
            self.sneak.append(Body(self.game, index, self.sneak[len(self.sneak)-1].last_pos, self.sneak[len(self.sneak)-1].dir, self.sneak[len(self.sneak)-2].dir))
        elif index>0:
            self.sneak.append(Body(self.game, index, self.sneak[len(self.sneak) - 1].last_pos, self.sneak[len(self.sneak) - 1].dir, self.head.dir))

    def spawn_apple(self):
        self.apple_pos = Vector2(randint(0, self.matrix_size.x - 1), randint(0, self.matrix_size.y - 1))
        for i in range(len(self.sneak)):
            if(self.apple_pos.x == self.sneak[i].pos.x and self.apple_pos.y == self.sneak[i].pos.y):
                self.spawn_apple()
                break
        if (self.apple_pos.x == self.head.pos.x and self.apple_pos.y == self.head.pos.y):
            self.spawn_apple()

    def apple_draw(self):
        real_pos_x = self.apple_pos.x * self.field_size.x + self.draw_start_pos.x
        real_pos_y = self.apple_pos.y * self.field_size.y + self.draw_start_pos.y
        rect = pygame.Rect(real_pos_x,real_pos_y,self.field_size.x,self.field_size.y)
        self.game.screen.blit(self.apple_image, rect)

    def background_draw(self):
        real_pos_x = 0
        real_pos_y = 0
        rect = pygame.Rect(real_pos_x, real_pos_y, int(self.screen_size[0]*self.background_size), int(self.screen_size[1]*self.background_size))
        self.game.screen.blit(self.background_image, rect)

    def foreground_draw(self):
        real_pos_x = 0
        real_pos_y = 0
        rect = pygame.Rect(real_pos_x, real_pos_y, int(self.screen_size[0]*self.background_size), int(self.screen_size[1]*self.background_size))
        self.game.screen.blit(self.foreground_image, rect)

    def score_draw(self):
        font = pygame.font.Font("Data/pixel.ttf", 35)
        text = font.render("Score:", 0, (69, 69, 69))
        score = font.render(str(self.points), 0, (69, 69, 69))
        pos_x = (self.game.screen.get_size()[0]) - text.get_rect().width*1.7
        pos_y = 12
        self.game.screen.blit(text, (pos_x, pos_y))
        self.game.screen.blit(score, (pos_x+text.get_rect().width, pos_y))

    def draw_border(self):
        for x in range(int(self.matrix_size.x)+1):
            pygame.draw.line(self.game.screen, self.border_color, (x*self.field_size.x, 0)+self.draw_start_pos, (x*self.field_size.x, self.matrix_size.y*self.field_size.y)+self.draw_start_pos)
        for y in range(int(self.matrix_size.y)+1):
            pygame.draw.line(self.game.screen, self.border_color, (0, y*self.field_size.y)+self.draw_start_pos, (self.matrix_size.x*self.field_size.x, y*self.field_size.y)+self.draw_start_pos)

    def draw_edge(self):
        pygame.draw.line(self.game.screen, self.border_color, self.draw_start_pos,(0, self.matrix_size.y * self.field_size.y) + self.draw_start_pos)
        pygame.draw.line(self.game.screen, self.border_color, self.draw_start_pos,(self.matrix_size.x * self.field_size.x, 0) + self.draw_start_pos)
        pygame.draw.line(self.game.screen, self.border_color, (self.matrix_size.x * self.field_size.x, 0)+self.draw_start_pos, (self.matrix_size.x * self.field_size.x, self.matrix_size.y * self.field_size.y) + self.draw_start_pos)
        pygame.draw.line(self.game.screen, self.border_color, (0, self.matrix_size.y * self.field_size.y)+self.draw_start_pos, (self.matrix_size.x * self.field_size.x, self.matrix_size.y * self.field_size.y) + self.draw_start_pos)

    def game_over_draw(self):
        color = (200,80,80)
        pos_x = self.game.screen.get_size()[0]/2
        pos_y = self.game.screen.get_size()[1]/2
        font_1 = pygame.font.Font("Data/pixel.ttf", 80)
        font_2 = pygame.font.Font("Data/pixel.ttf", 30)
        text_rend_1 = font_1.render("Game Over", 2, color)
        text_rend_2 = font_2.render("press enter to play again", 2, color)
        text_rend_3 = font_2.render("or escape to exit to main menu", 2, color)
        interline = 150
        self.game.screen.blit(text_rend_1, (pos_x - text_rend_1.get_rect().width / 2.0, pos_y - interline / 2 - text_rend_1.get_rect().height / 2.0))
        self.game.screen.blit(text_rend_2, (pos_x - text_rend_2.get_rect().width / 2.0, pos_y - text_rend_2.get_rect().height / 2.0))
        self.game.screen.blit(text_rend_3, (pos_x - text_rend_3.get_rect().width / 2.0, pos_y + interline / 2 - text_rend_3.get_rect().height / 2.0))

        # Inputs
        press = pygame.key.get_pressed()
        if press[pygame.K_RETURN]:
            self.game.plane = Matrix(self.game, self.States)
            self.game.current_state = self.States.GAME
        if press[pygame.K_ESCAPE]:
            self.game.current_state = self.States.MENU


    def tick(self):
        self.head.set_dir()
        for i in range(len(self.sneak)):
            self.sneak[len(self.sneak)-1-i].tick()
        self.head.tick()
        self.head.check_if_crash()

    def draw(self):
        self.background_draw()
        self.draw_border()
        self.points = len(self.sneak) - 1
        if(self.points > self.game.menu.highscore_score):
            d = shelve.open('Data/score.txt')
            d['score'] = self.game.menu.highscore_score
            d.close()
            self.game.menu.highscore_score = self.points
        self.draw_edge()
        self.apple_draw()
        for i in range(len(self.sneak)):
            self.sneak[i].draw()
        self.head.draw()
        self.foreground_draw()
        self.score_draw()
