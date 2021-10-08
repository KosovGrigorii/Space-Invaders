import os

import pygame
import shelve
from pygame import mixer

from Dead_script import DeadScreen
from Game_script import Game


class Menu:
    Level_dict = {
        "A": (pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "InvaderA1.png")), (36, 36)), 10),
        "B": (pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "InvaderB1.png")), (36, 36)), 20),
        "C": (pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "InvaderC1.png")), (36, 36)), 30),
        "D": (pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "SpaceInvaders.png")), (72, 36)), 50)
    }
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.width, self.height = game.width, game.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.click_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "click.mp3"))
        self.click_sound.set_volume(0.5)

        self.start_button = pygame.Rect(self.width/2-100, self.height/2 - 60, 200, 50)
        self.name_rect = pygame.Rect(self.width / 2 - self.width / 4, self.height / 10, self.width / 2, self.height / 10)
        self.best_score_rect = pygame.Rect(self.width - self.width / 4, self.height - self.height / 10,
                                           self.width / 9, self.height / 20)
        self.running = True
        self.playing = False
        self.score = 0
        d = shelve.open('score.txt')
        if d.__contains__('score'):
            self.score = d['score']  # the score is read from disk
        else:
            d['score'] = self.score
        d.close()

    def display_menu(self):
        self.running = True
        click = False

        while self.running:
            self.screen.fill((0, 0, 0))

            self.draw_text("SPACE INVADERS", self.name_rect)
            self.draw_text("START", self.start_button)
            self.display_invaders_range(self.width/2-80, self.height/2 + 10)
            self.draw_text(f"BEST SCORE : {self.score}", self.best_score_rect)
            self.check_if_clicked(click)

            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.clock.tick(60)

    def check_if_clicked(self, click):
        mx, my = pygame.mouse.get_pos()
        if self.start_button.collidepoint(mx, my):
            if click:
                self.click_sound.play()
                self.game.game_loop()
                if not self.game.menu_running:
                    self.running = False
                    return
                dead_screen = DeadScreen(self, self.game)
                dead_screen.display_dead_screen()
                if self.score < self.game.player.score:
                    self.score = self.game.player.score
                d = shelve.open('score.txt')  # here you will save the score variable
                d['score'] = self.score  # thats all, now it is saved on disk.
                d.close()
                self.game = Game(900, 600)
            else:
                self.draw_text("START", self.start_button, color=(10, 255, 4))



    def draw_text(self, text, rect, color=(255,255,255)):
        pygame.draw.rect(self.screen, (0,0,0), rect)
        self.game.display_text(text, rect.height, rect.centerx,
                               rect.centery, self.screen, color)

    def draw_image(self, pic, centerx, centery):
        self.game.screen.blit(pic, (centerx, centery))

    def display_invaders_range(self,  centerx, centery):
        for elem in self.Level_dict.values():
            pic, level = elem[0], elem[1]
            self.draw_image(pic, centerx-pic.get_width()/2, centery)
            self.draw_text(":  " + str(level), pygame.Rect(centerx+105, centery, 20, 40))
            centery += 60







if __name__ == '__main__':
    menu = Menu(Game(900, 600))