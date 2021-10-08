import os

import pygame
import shelve
from pygame import mixer

from Game_script import Game


class DeadScreen:
    def __init__(self, menu, game):
        pygame.init()
        self.game = game
        self.menu = menu
        self.width, self.height = game.width, game.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.click_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "click.mp3"))
        self.click_sound.set_volume(0.5)

        self.start_button = pygame.Rect(self.width/2-100, self.height/2 - 60, 200, 50)
        self.name_rect = pygame.Rect(self.width / 2 - self.width / 4, self.height / 10, self.width / 2, self.height / 10)
        self.best_score_rect = pygame.Rect(self.width/2-100, self.height/2, 200, 50)
        self.hint_score = pygame.Rect(self.width/2-100, self.height/2 + 60, 200, 50)

        self.running = True
        self.playing = False
        self.score = 0
        d = shelve.open('score.txt')
        if d.__contains__('score'):
            self.score = d['score']  # the score is read from disk
        else:
            d['score'] = self.score
        d.close()

    def display_dead_screen(self):
        self.running = True
        click = False

        while self.running:
            self.screen.fill((0, 0, 0))

            self.menu.draw_text("YOU LOST", self.name_rect)
            self.menu.draw_text(f"YOUR SCORE : {self.game.player.score}", self.start_button)
            self.menu.draw_text(f"BEST SCORE : {self.score}", self.best_score_rect)
            self.menu.draw_text(f"<<<PRESS SPACE>>>", self.hint_score)

            click = False

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.click_sound.play()
                    self.running = False
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.clock.tick(60)