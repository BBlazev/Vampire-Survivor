import pygame
import sys
from player import Player
from enemy import spawn_enemy  
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SPAWN_INTERVAL, BG_COLOR, game_over
from camera import Camera
from background import InfiniteBackground
from heart import *

ENEMY_KILLED_EVENT = pygame.USEREVENT + 2
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vampire Survivors")
    clock = pygame.time.Clock()

    tileset = pygame.image.load("assets/Background/background.png").convert_alpha()
    grass_tile = InfiniteBackground.get_tile(tileset, 0, 0, 16, 16)
    background = InfiniteBackground(grass_tile)

    camera = Camera()
    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

    score = 0
    font = pygame.font.SysFont(None, 36)
    heart_states = load_heart_states()  

    while True:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == SPAWN_EVENT and not game_over:
                enemy = spawn_enemy(player)
                enemies.add(enemy)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over:
                    player.attack()
            elif event.type == ENEMY_KILLED_EVENT:
                score += 1  

        if not game_over:
            player.update(keys_pressed, enemies)
            enemies.update()

        camera.update(player)

        background.draw(screen, camera)

        screen.blit(player.image, camera.apply(player))
        for enemy in enemies:
            screen.blit(enemy.image, camera.apply(enemy))
            enemy_rect_debug = enemy.rect.copy()
            enemy_rect_debug.x -= camera.camera.x
            enemy_rect_debug.y -= camera.camera.y
            pygame.draw.rect(screen, (0, 255, 0), enemy_rect_debug, 2)

        for proj in projectiles:
            screen.blit(proj.image, camera.apply(proj))

        if player.attacking and hasattr(player, 'attack_rect'):
            debug_rect = player.attack_rect.copy()
            debug_rect.x -= camera.camera.x
            debug_rect.y -= camera.camera.y
            pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        if game_over:
            over_text = font.render("GAME OVER", True, (255, 255, 255))
            text_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(over_text, text_rect)
        #draw_health_ui(screen, player.health, 20, heart_states, (10, 10))

        pygame.display.flip()

if __name__ == '__main__':
    main()
