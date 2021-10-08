import os
import random
from pygame import mixer

import pygame

class Block:
    quality = {
        "Healthy": pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "OkBlock.png")), (28, 20)),
        "Wounded": pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "WeakBlock.png")), (28, 20))
    }

    def __init__(self, game, x, y, frame):
        self.pic = self.quality["Healthy"]
        self.x = x
        self.game = game
        self.y = y
        self.mask = pygame.mask.from_surface(self.pic)
        self.frame = frame

    def draw(self):
        self.game.screen.blit(self.pic, (self.x, self.y))

    def checkCollision(self, game):
        for rocket in game.alien_rocket:
            offset_x = self.x - rocket.x
            offset_y = self.y - rocket.y
            if rocket.mask.overlap(self.mask, (int(offset_x), int(offset_y))) is not None:
                try:
                    game.alien_rocket.remove(rocket)
                    if self.pic == self.quality["Wounded"]:
                        self.frame.blocks.remove(self)
                        #game.block_frames.remove(self)
                    else:
                        self.pic = self.quality["Wounded"]
                except Exception:
                    break

        for rocket in game.player_rockets:
            offset_x = self.x - rocket.x
            offset_y = self.y - rocket.y
            if rocket.mask.overlap(self.mask, (int(offset_x), int(offset_y))) is not None:
                try:
                    game.player_rockets.remove(rocket)
                except Exception:
                    break


class BlockGenerator:

    def __init__(self, game):
        self.margin = 30
        self.width = 168
        self.interval = 42
        self.game = game
        self.height = game.player.y - 60

        for x in range(self.margin, game.width - self.margin, self.width):
            game.block_frames.append(BlockFrame(game, x + self.interval, game.player.y - 60))

    def draw(self, game):
        for x in range(self.margin, game.width - self.margin, self.width):
            game.block_frames.append(BlockFrame(game, x + self.interval, game.player.y - 60))


class BlockFrame:
    x_intervals = [0, 0, 28, 56, 56]
    y_intervals = [+20, 0, 0, 0, +20]

    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.blocks = []
        self.fill()

    def draw(self):
        for block in self.blocks:
            block.draw()
            block.checkCollision(self.game)

    def fill(self):
        for i in range(5):
            self.blocks.append(Block(self.game, self.x + self.x_intervals[i], self.y + self.y_intervals[i], self))


