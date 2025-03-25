import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class InfiniteBackground:
    def __init__(self, tile_image: pygame.Surface):
        """
        Expects a single tile (Surface) that will be repeated.
        """
        self.tile_image = tile_image
        self.tile_width = tile_image.get_width()
        self.tile_height = tile_image.get_height()

    def draw(self, screen, camera):
        """
        Draw the single tile repeatedly to fill the screen,
        offset by the camera's position.
        """

        x_offset = camera.camera.x % self.tile_width
        y_offset = camera.camera.y % self.tile_height

        tiles_x = SCREEN_WIDTH // self.tile_width + 2
        tiles_y = SCREEN_HEIGHT // self.tile_height + 2

        for i in range(tiles_x):
            for j in range(tiles_y):
                x = -x_offset + i * self.tile_width
                y = -y_offset + j * self.tile_height
                screen.blit(self.tile_image, (x, y))

    @staticmethod
    def get_tile(sheet: pygame.Surface, x: int, y: int, width: int, height: int) -> pygame.Surface:
        """
        Extracts a sub-surface (tile) from the provided sheet and returns it.
        """
        rect = pygame.Rect(x, y, width, height)
        tile_image = sheet.subsurface(rect).copy()
        return tile_image
