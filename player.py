import pygame
from settings import *
import math
from projectile import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {}
        self.load_animations()
        
        self.current_state = "idle"
        self.frames = self.animations[self.current_state]
        self.frame_index = 0
        self.animation_speed = 100  
        self.last_update = pygame.time.get_ticks()
        self.facing_left = False

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.last_shot = pygame.time.get_ticks()

    def load_animations(self):
        """Load and slice sprite sheets for each state."""
        idle_sheet = pygame.image.load("assets/Idle/Player Idle.png").convert_alpha()
        self.animations["idle"] = [idle_sheet.subsurface((i * 48, 0, 48, 48))
                                   for i in range(10)]
        
        run_sheet = pygame.image.load("assets/Run/player run.png").convert_alpha()
        self.animations["run"] = [run_sheet.subsurface((i * 48, 0, 48, 48))
                                  for i in range(8)]
        
        attack_sheet = pygame.image.load("assets/Attack/player sword.png").convert_alpha()
        self.animations["attack"] = [attack_sheet.subsurface((i * 64, 0, 64, 64))
                                     for i in range(6)]

    def set_state(self, new_state):
        """Change the current animation state if not already in attack."""
        if self.current_state != "attack" and new_state != self.current_state:
            self.current_state = new_state
            self.frames = self.animations[self.current_state]
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()
            self.image = (pygame.transform.flip(self.frames[self.frame_index], True, False)
                          if self.facing_left else self.frames[self.frame_index])

    def attack(self):
        """Trigger the attack state regardless of movement.
           The attack animation plays fully while allowing movement.
        """
        self.current_state = "attack"
        self.frames = self.animations["attack"]
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.image = (pygame.transform.flip(self.frames[self.frame_index], True, False)
                      if self.facing_left else self.frames[self.frame_index])

    def handle_animation(self, keys_pressed):
        """Update the current animation frame, flipping the image if needed."""
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.animation_speed:
            self.last_update = now
            if self.current_state == "attack":
                if self.frame_index < len(self.frames) - 1:
                    self.frame_index += 1
                else:
                    if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a] or
                        keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d] or
                        keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w] or
                        keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]):
                        self.current_state = "run"
                    else:
                        self.current_state = "idle"
                    self.frames = self.animations[self.current_state]
                    self.frame_index = 0
            else:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
            
            current_frame = self.frames[self.frame_index]
            self.image = pygame.transform.flip(current_frame, True, False) if self.facing_left else current_frame

    def handle_movement(self, keys_pressed):
        """Process movement and update the facing direction."""
        dx, dy = 0, 0
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            dx = -PLAYER_SPEED
            self.facing_left = True  
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            dx = PLAYER_SPEED
            self.facing_left = False 
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            dy = PLAYER_SPEED

        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        if self.current_state != "attack":
            if dx != 0 or dy != 0:
                self.set_state("run")
            else:
                self.set_state("idle")

    def update(self, keys_pressed):
        """Update both animation and movement independently."""
        self.handle_animation(keys_pressed)
        self.handle_movement(keys_pressed)


    def auto_shoot(self, projectiles_group):
        """Automatically fire projectiles in eight directions, disabled during attack if desired."""
        if self.current_state != "attack":
            now = pygame.time.get_ticks()
            if now - self.last_shot >= AUTO_SHOOT_DELAY:
                self.last_shot = now
                for angle in range(0, 360, 45):
                    rad = math.radians(angle)
                    dx = math.cos(rad) * PROJECTILE_SPEED
                    dy = math.sin(rad) * PROJECTILE_SPEED
                    projectile = Projectile(self.rect.center, dx, dy)
                    projectiles_group.add(projectile)
