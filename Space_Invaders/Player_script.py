import os
import pygame
from pygame import mixer

class Player:
    def __init__(self, game, x, y):
        pygame.init()
        self.x = x
        self.game = game
        self.y = y
        self.pic = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "Ship.png")), (60, 40))
        self.lifecount = 3
        self.mask = pygame.mask.from_surface(self.pic)
        self.score = 0
        self.hit_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "ShipHit.wav"))
        self.hit_sound.set_volume(0.05)
        self.dead_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "explosion.wav"))
        self.dead_sound.set_volume(0.1)


    def draw(self):
        self.game.screen.blit(self.pic, (self.x, self.y))
        if self.lifecount <= 0:
            self.game.stop_game()

    def damaged(self):
        self.lifecount -= 1
        #if self.lifecount == 0:

    def checkCollision(self, game):
        for rocket in game.alien_rocket:
            offset_x = self.x - rocket.x
            offset_y = self.y - rocket.y
            if rocket.mask.overlap(self.mask, (int(offset_x), int(offset_y))) is not None:
                try:
                    self.lifecount -= 1
                    if self.lifecount == 0:
                        self.dead_sound.play()
                    else:
                        self.hit_sound.play()
                    game.alien_rocket.remove(rocket)
                except Exception:
                    break

    def player_move(self, game):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.x -= 2 if self.x > 20 else 0
        elif pressed[pygame.K_RIGHT]:
            self.x += 2 if self.x < game.width - 80 else 0


