
import pygame
import  os


class Rocket:
    def __init__(self, game, x, y, owner=None, picture=None):
        pygame.init()
        self.Sound_dict = {
            "Player": pygame.mixer.Sound(os.path.join("assets/sounds", "ShipBullet.wav")),
            "Invader": pygame.mixer.Sound(os.path.join("assets/sounds", "InvaderBullet.wav"))
        }
        self.x = x
        self.y = y
        self.game = game
        if picture is None:
            self.pic = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "Bullet.png")), (3, 6))
        else:
            self.pic = picture
        self.mask = pygame.mask.from_surface(self.pic)
        if owner is not None:
            self.bullet_sound = self.Sound_dict[owner]
            self.bullet_sound.set_volume(0.02)
            self.bullet_sound.play()


    def draw(self, moving_index, sequence):
        self.game.screen.blit(self.pic, (self.x, self.y))
        self.y += moving_index
        if self.y > self.game.height:
            sequence.remove(self)
