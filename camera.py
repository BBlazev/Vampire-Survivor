import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self):
        # Initialize with a view that matches the screen dimensions.
        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def apply(self, target):
        """
        Returns a rect with the target's position offset by the camera's position.
        Use this when drawing the target so it appears in the correct position.
        """
        return target.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        """
        Center the camera on the target without clamping, for an infinite map.
        """
        x = target.rect.centerx - SCREEN_WIDTH // 2
        y = target.rect.centery - SCREEN_HEIGHT // 2
        self.camera = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)
