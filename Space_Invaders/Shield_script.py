import os
import pygame

class Shield:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.strengthCount = 1

    def draw(self):
        pic = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "OkBlock.png")), (45, 30))
        self.game.screen.blit(pic, (self.x, self.y))

    def damage(self):
        if self.strengthCount == 1:
            pic = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "WeakBlock.png")), (45, 30))
            self.game.screen.blit(pic, (self.x, self.y))
            self.strengthCount = 0
        else:
            del(self)
