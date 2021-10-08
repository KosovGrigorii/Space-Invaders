import os
import random
from pygame import mixer

import pygame

from Rocket_script import Rocket


class Alien:
    Level_dict = {
        "A": (pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "InvaderA1.png")), (40, 40)), 10),
        "B": (pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "InvaderB1.png")), (40, 40)), 20),
        "C": (pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "InvaderC1.png")), (40, 40)), 30)
    }


    def __init__(self, game, x, y, level, xcoef):
        pygame.init()
        self.pic, self.level = self.Level_dict[level]
        self.x = x
        self.game = game
        self.y = y
        #self.size = 30
        self.bothsides = 2
        self.xcoef = xcoef
        self.mask = pygame.mask.from_surface(self.pic)
        self.hit_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "InvaderHit.wav"))
        self.hit_sound.set_volume(0.05)

    def draw(self):
        self.game.screen.blit(self.pic, (self.x, self.y))


    def checkCollision(self, game):
        for rocket in game.player_rockets:
            offset_x = self.x - rocket.x
            offset_y = self.y - rocket.y
            if rocket.mask.overlap(self.mask, (int(offset_x), int(offset_y))) is not None:
                try:
                    self.hit_sound.play()
                    game.player_rockets.remove(rocket)
                    game.aliens.remove(self)
                    game.player.score += self.level
                except Exception:
                    break


acceleration = 1.1


class Generator:

    def __init__(self, game, margin, xcoef):
        self.bullet_pic = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "InvaderBullet.png")),
                                                 (7, 20))
        self.speed = -0.5
        width = 50
        self.game = game
        level_list = ["C", "B", "B", "A", "A"]
        num = 0
        ammount_of_rows = 5

        for y in range(margin, int(game.height / 2), width):
            for x in range(margin + 70, game.width - margin, width):
                game.aliens.append(Alien(game, x, y, level_list[num], self.speed*xcoef))
            if num < len(level_list) - 1:
                num += 1
            else:
                break

    def move(self):
        flag = True
        for elem in self.game.aliens:
            if elem.x <= 5:
                for elem1 in self.game.aliens:
                    elem1.bothsides = 1

                    elem1.xcoef *= -1
                    elem1.x += elem1.xcoef
                flag = False
                break

            elif elem.bothsides == 0:
                for elem1 in self.game.aliens:
                    elem1.x += elem1.xcoef
                    elem1.bothsides = 2
                flag = False
                break

            elif elem.x >= self.game.width - 40:
                for elem1 in self.game.aliens:
                    elem1.y += 5
                    elem1.bothsides = 0

                    if elem1.xcoef <= 3.5:
                        elem1.xcoef *= -acceleration

                    else:
                        elem1.xcoef *= -1
                flag = False
                break

        if flag:
            for elem1 in self.game.aliens:
                elem1.x += elem1.xcoef

    def shoot(self, alien_rocket, aliens):
        if len(alien_rocket) == 0 and len(aliens) != 0:
            index = random.randint(0, len(aliens) - 1)
            alien_rocket.append(Rocket(self.game, aliens[index].x + 22.5, aliens[index].y, picture=self.bullet_pic))

        elif len(aliens) != 0:
            alien_rocket[0].draw(2, alien_rocket)