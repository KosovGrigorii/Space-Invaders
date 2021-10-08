import pygame
import os


class LivesDisplay:
    def __init__(self, game):
        self.pic = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "Ship.png")), (39, 26))
        self.game = game
        self.mask = pygame.mask.from_surface(self.pic)

    def draw(self, lives_count):
        width = 10
        for i in range(lives_count):
            self.game.screen.blit(self.pic, (width, self.game.height - 30))
            width += 49
