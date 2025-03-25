import pygame
from settings import *  

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {}
        self.load_animations()
        
        self.current_state = "idle"
        self.frames = self.animations[self.current_state]
        self.frame_index = 0

        self.normal_animation_speed = 100  
        self.attack_animation_speed = 50   
        self.last_update = pygame.time.get_ticks()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.facing_right = True

        self.attack_damage = 10
        self.attacking = False
        self.damage_applied = False  

        self.health = 100


    def load_animations(self):
        scale_factor = 2 

        idle_sheet = pygame.image.load("assets/Idle/Player Idle.png").convert_alpha()
        self.animations["idle"] = [
            pygame.transform.scale(
                idle_sheet.subsurface((i * 48, 0, 48, 48)),
                (int(48 * scale_factor), int(48 * scale_factor))
            ) for i in range(10)
        ]
        
        run_sheet = pygame.image.load("assets/Run/player run.png").convert_alpha()
        self.animations["run"] = [
            pygame.transform.scale(
                run_sheet.subsurface((i * 48, 0, 48, 48)),
                (int(48 * scale_factor), int(48 * scale_factor))
            ) for i in range(8)
        ]
        
        attack_sheet = pygame.image.load("assets/Attack/player sword.png").convert_alpha()
        self.animations["attack"] = [
            pygame.transform.scale(
                attack_sheet.subsurface((i * 64, 0, 64, 64)),
                (int(64 * scale_factor), int(64 * scale_factor))
            ) for i in range(6)
        ]

    def set_state(self, new_state):
        if new_state != self.current_state:
            self.current_state = new_state
            self.frames = self.animations[self.current_state]
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()
            self.image = self.frames[self.frame_index]

    def attack(self):
        self.set_state("attack")
        self.attacking = True
        self.damage_applied = False

    def take_damage(self, damage):
        self.health -= damage
        print("Player health:", self.health)
        if self.health <= 0:
            self.health = 0
            print("Player died!")
            game_over = True

    def update(self, keys_pressed, enemy_group=None):
        now = pygame.time.get_ticks()
        current_speed = self.attack_animation_speed if self.current_state == "attack" else self.normal_animation_speed
        dt = now - self.last_update

        if dt >= current_speed:
            frames_to_advance = dt // current_speed
            self.frame_index += frames_to_advance
            self.last_update = now - (dt % current_speed)

            if self.current_state == "attack":
                if self.frame_index >= len(self.frames):
                    self.set_state("idle")
                    self.attacking = False
                else:
                    hit_frame = 5  
                    if self.frame_index == hit_frame and not self.damage_applied and enemy_group is not None:
                        self.attack_rect = self.rect.copy()
                        extension = 40  
                        if self.facing_right:
                            self.attack_rect.width += extension
                        else:
                            self.attack_rect.x -= extension
                            self.attack_rect.width += extension

                        for enemy in enemy_group:
                            if self.attack_rect.colliderect(enemy.rect):
                                if hasattr(enemy, "take_damage"):
                                    enemy.take_damage(self.attack_damage)
                                else:
                                    enemy.health -= self.attack_damage
                        self.damage_applied = True
            else:
                self.frame_index %= len(self.frames)

            self.image = self.frames[self.frame_index % len(self.frames)]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

        if not self.attacking:
            movement = pygame.math.Vector2(0, 0)
            if keys_pressed[pygame.K_a]:
                movement.x -= PLAYER_SPEED
            if keys_pressed[pygame.K_d]:
                movement.x += PLAYER_SPEED
            if keys_pressed[pygame.K_w]:
                movement.y -= PLAYER_SPEED
            if keys_pressed[pygame.K_s]:
                movement.y += PLAYER_SPEED

            if movement.x < 0:
                self.facing_right = False
            elif movement.x > 0:
                self.facing_right = True

            if movement.length() > 0:
                self.rect.x += movement.x
                self.rect.y += movement.y
                self.set_state("run")
            else:
                self.set_state("idle")