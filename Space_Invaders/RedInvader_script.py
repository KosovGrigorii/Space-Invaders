import os
import random

import pygame
from pygame import mixer


class RedInvader:
    pic = pygame \
        .transform \
        .scale(pygame.image.load(os.path.join("assets/images", "SpaceInvaders.png")), (72, 36))

    def __init__(self, game, x, y, ind):
        self.level = 50
        self.x = x
        self.game = game
        self.y = y
        self.mask = pygame.mask.from_surface(self.pic)
        self.move_x_coef = 3.0
        self.move_y_coef = 1.5
        self.ind = ind
        self.move_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "ufo_highpitch.wav"))
        self.move_sound.set_volume(0.05)
        self.hit_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "InvaderHit.wav"))
        self.hit_sound.set_volume(0.5)

    def draw(self):
        self.game.screen.blit(self.pic, (self.x, self.y))

    def Move(self, game):
        self.x += self.move_x_coef*self.ind
        self.y += self.move_y_coef

    def checkCollision(self, game):
        for rocket in game.player_rockets:
            offset_x = self.x - rocket.x
            offset_y = self.y - rocket.y
            if rocket.mask.overlap(self.mask, (int(offset_x), int(offset_y))) is not None:
                try:
                    self.move_sound.stop()
                    self.hit_sound.play()
                    game.player_rockets.remove(rocket)
                    game.player.score += self.level
                    return True
                except Exception:
                    break

    def generate_red_invader(self, game):
        self.move_sound.play(-1)
        self.draw()
        self.Move(game)
        if self.checkCollision(game) or self.x > game.width or self.y > game.height:
            self.move_sound.stop()
            return self.choose_side(game)
        return 0, 0

    def choose_side(self, game):
        x = random.choice((-72, game.width + 72))
        ind = 1
        if x > 0:
            ind = -1

        return x, ind


