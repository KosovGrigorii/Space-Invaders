# This is a sample Python script.

import os
import random
from pygame import mixer

# /Users/grigorijkosov/PycharmProjects/Space_Invaders/
import pygame

from Alien_script import Generator
from Block_Script import BlockGenerator
from Player_script import Player
from RedInvader_script import RedInvader
from Rocket_script import Rocket
from lives_display import LivesDisplay


class Game:
    screen = None
    aliens = []
    block_frames = []
    player_rockets = []
    alien_rocket = []

    def __init__(self, width, height):
        pygame.init()
        self.margin = 30
        self.level = 1
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.redind = random.randrange(1, 1000)
        self.done = False
        self.redInvaders = RedInvader(self, -72, -36, 1)

        self.player = Player(self, width / 2, height - 89)
        self.generator = Generator(self, self.margin, 1)
        self.block_generator = BlockGenerator(self)
        self.live_display = LivesDisplay(self)
        self.menu_running = True

        #self.game_loop()


    def game_loop(self):
        while not self.done:

            self.screen.fill((0, 0, 0))

            if len(self.aliens) == 0:
                self.level += 1
                self.generator = Generator(self, self.margin*self.level, 1 + float(self.level/10))
                self.block_frames.clear()
                self.block_generator = BlockGenerator(self)

            self.draw_bottom_line()
            self.player.player_move(self)

            # RedInvader block
            if self.redind >= 999:
                is_red_killed_x, is_red_killed_ind,  = self.redInvaders.generate_red_invader(self)
                if is_red_killed_ind != 0:
                    self.redInvaders = RedInvader(self, is_red_killed_x, -36, is_red_killed_ind)
                    self.redind = random.randrange(1, 1000)

            else:
                self.redind = random.randrange(1, 1000)
            #RedInvader end

            for block_frame in self.block_frames:
                block_frame.draw()

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > self.block_generator.height - 40):
                    self.stop_game()

            self.generator.shoot(self.alien_rocket, self.aliens)

            self.generator.move()

            for rocket in self.player_rockets:
                rocket.draw(-2, self.player_rockets)

            self.get_key()
            self.clock.tick(60)
            pygame.display.update()

    def display_text(self, tex, fontsize, centerx, centery, screen, color=(255, 255, 255)):
        pygame.font.init()
        font = pygame.font.Font(os.path.join("assets/fonts", "unifont.ttf"), fontsize)
        text = font.render(tex, False, color)

        text_rect = text.get_rect(center=(centerx, centery))
        screen.blit(text, text_rect)

    def get_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_game()
                self.menu_running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.click_sound.play()
                self.stop_game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player_rockets.append(Rocket(self, self.player.x + 30, self.player.y, "Player"))

    def stop_game(self):
        self.done = True
        self.aliens.clear()
        self.block_frames.clear()
        self.player_rockets.clear()
        self.alien_rocket.clear()
        self.redInvaders.generate_red_invader(self, True)

    def draw_bottom_line(self):
        self.display_text(f"Score : {self.player.score}", 39, (self.width - 200), (self.height - 22), self.screen)
        self.live_display.draw(self.player.lifecount)
        self.player.draw()
        if self.player.lifecount <= 0:
            self.stop_game()
        self.player.checkCollision(self)


if __name__ == '__main__':
    game = Game(900, 600)
