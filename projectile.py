import pygame
from settings import *
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy):
        """Initialize a projectile moving with the given velocity."""
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PROJECTILE_COLOR, (4, 4), 4)
        self.rect = self.image.get_rect(center=pos)
        self.dx = dx
        self.dy = dy

    def update(self):
        """Move the projectile and remove it if it goes off-screen."""
        self.rect.x += self.dx
        self.rect.y += self.dy
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).contains(self.rect):
            self.kill()
