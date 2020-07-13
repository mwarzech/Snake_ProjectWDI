import pygame,sys
from src.matrix import Matrix
from pygame.math import Vector2
import shelve


class Menu(object):
    def __init__(self, game, states):
        self.game = game
        self.button_normal_color = (149,215,0)
        self.button_highlight_color = (139,199,0)
        self.font = pygame.font.Font("Data/pixel.ttf", 75)
        self.buttons = [[None]*6,[None]*6]
        self.States = states

        # Title config
        self.title_image = pygame.image.load("Data/snakeLogo.png")
        self.title_size = Vector2(80,48)*4
        self.title_image = pygame.transform.scale(self.title_image, (int(self.title_size.x), int(self.title_size.y)))
        #self.title_font = pygame.font.SysFont("Monospace",120,True)
        #self.title_rend = self.title_font.render("Snake", 2, (50, 120, 10))
        self.title_pos_x = (self.game.screen.get_size()[0] / 2.0) - self.title_size.x/2.0
        self.title_pos_y = (self.game.screen.get_size()[1] / 4.0) - self.title_size.y/ 2.0
        self.title_rect = pygame.Rect(self.title_pos_x, self.title_pos_y, self.title_size.x, self.title_size.y)

        # Start button config
        self.buttons[0][5] = pygame.image.load("Data/PlayDefault.png")  # current img
        self.buttons[0][4] = pygame.image.load("Data/PlayPressed.png")
        self.buttons[0][3] = pygame.image.load("Data/PlayDefault.png")
        self.buttons[0][2] = Vector2(256, 128)
        self.buttons[0][1] = (2.0*self.game.screen.get_size()[1] / 4.0) - (self.buttons[0][2].y / 2.0)
        self.buttons[0][0] = (self.game.screen.get_size()[0] / 2.0) - (self.buttons[0][2].x / 2.0)

        # Quit button config
        self.buttons[1][5] = pygame.image.load("Data/QuitDefault.png")  # current img
        self.buttons[1][4] = pygame.image.load("Data/QuitPressed.png")
        self.buttons[1][3] = pygame.image.load("Data/QuitDefault.png")
        self.buttons[1][2] = Vector2(256, 128)
        self.buttons[1][1] = (3.0*self.game.screen.get_size()[1] / 4.0) - (self.buttons[0][2].y / 2.0)
        self.buttons[1][0] = (self.game.screen.get_size()[0] / 2.0) - (self.buttons[0][2].x / 2.0)

        #HighScore config
        try:
            d = shelve.open('Data/score.txt')
            self.highscore_score = d['score']
        except Exception:
            self.highscore_score = 0

        pygame.mixer.music.stop()


    def highscore_draw(self):
        pos_x = (4.0 * self.game.screen.get_size()[0] / 5.0)
        pos_y = (14.0 * self.game.screen.get_size()[1] / 15.0)
        font = pygame.font.Font("Data/pixel.ttf", 50)
        text_rend = font.render("Highscore: "+str(self.highscore_score), 2, (69, 69, 69))
        self.game.screen.blit(text_rend, (pos_x - text_rend.get_rect().width / 2.0,pos_y - text_rend.get_rect().height / 2.0))

    def title_draw(self):
        self.game.screen.blit(self.title_image, self.title_rect)

    def button_draw(self, index):
        self.buttons[index][5] = pygame.transform.scale(self.buttons[index][5], (int(self.buttons[index][2].x), int(self.buttons[index][2].y)))
        rect = pygame.Rect(self.buttons[index][0], self.buttons[index][1], self.buttons[index][2].x, self.buttons[index][2].y)
        self.game.screen.blit(self.buttons[index][5], rect)

    def check_mouse_pos(self):
        for i in range(len(self.buttons)):
            left_border = self.buttons[i][0]
            right_border = self.buttons[i][0]+self.buttons[i][2].x
            up_border = self.buttons[i][1]
            down_border = self.buttons[i][1] + self.buttons[i][2].y
            if(self.mouse_x>=left_border and self.mouse_x<=right_border and self.mouse_y>=up_border and self.mouse_y<=down_border):
                self.buttons[i][5] = self.buttons[i][4]
                if(pygame.mouse.get_pressed()[0]):
                    self.button_action(i)
            else:
                self.buttons[i][5] = self.buttons[i][3]

    def button_action(self, index):
        if(index == 0):
            self.game.plane = Matrix(self.game, self.States)
            self.game.current_state = self.States.GAME
        elif(index == 1):
            sys.exit(0)

    def tick(self):
        pass

    def draw(self):
        self.mouse_x,self.mouse_y = pygame.mouse.get_pos()
        self.check_mouse_pos()
        for i in range(len(self.buttons)):
            self.button_draw(i)
        self.title_draw()
        self.highscore_draw()

