import pygame
import sys
import random
import math
from player import *
from enemy import *



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vampire Survivors")
    clock = pygame.time.Clock()

    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

    score = 0
    font = pygame.font.SysFont(None, 36)
    game_over = False

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

        if not game_over:
            player.update(keys_pressed)
            enemies.update()
            
            #projectiles.update()

            collisions = pygame.sprite.groupcollide(enemies, projectiles, True, True)
            score += len(collisions)

            #if pygame.sprite.spritecollideany(player, enemies):
            #    game_over = True

        screen.fill(BG_COLOR)
        screen.blit(player.image, player.rect)
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)
        for proj in projectiles:
            screen.blit(proj.image, proj.rect)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if game_over:
            over_text = font.render("GAME OVER", True, (255, 255, 255))
            text_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(over_text, text_rect)

        pygame.display.flip()

if __name__ == '__main__':
    main()

