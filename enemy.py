import pygame
from settings import *
import math
from projectile import *
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, target):
        """Initialize an enemy that will move toward the target (player)."""
        super().__init__()
        self.target = target  
        self.animations = {}
        self.load_animations()

        self.current_state = "run"
        self.frames = self.animations[self.current_state]
        self.frame_index = 0
        self.animation_speed = 100  
        self.last_update = pygame.time.get_ticks()
        self.facing_left = False

  
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def load_animations(self):
        run_sheet = pygame.image.load("assets/Enemy/Knight/Run.png").convert_alpha()
        run_frames = 8  
        sheet_width, sheet_height = run_sheet.get_size()
        frame_width = sheet_width // run_frames  
        self.animations["run"] = [
            run_sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
            for i in range(run_frames)
        ]
        attack_sheet = pygame.image.load("assets/Enemy/Knight/Attack.png").convert_alpha()
        att_frames = 22  
        sheet_width, sheet_height = attack_sheet.get_size()
        frame_width = sheet_width // att_frames
        self.animations["attack"] = [
            attack_sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
            for i in range(att_frames)
        ]

    def set_state(self, new_state):
        """Change the current animation state if not interrupted by an attack."""
        if self.current_state != "attack" and new_state != self.current_state:
            self.current_state = new_state
            self.frames = self.animations[self.current_state]
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()
            self.image = (pygame.transform.flip(self.frames[self.frame_index], True, False)
                          if self.facing_left else self.frames[self.frame_index])

    def attack(self):
        """Set the enemy to the attack state."""
        self.current_state = "attack"
        self.frames = self.animations["attack"]
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.image = (pygame.transform.flip(self.frames[self.frame_index], True, False)
                      if self.facing_left else self.frames[self.frame_index])

    def update(self):
        """Update enemy behavior:
           - If within ATTACK_RANGE, trigger attack and freeze movement.
           - Otherwise, move toward the player.
           - In all cases, update the animation using delta time.
        """
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1

        self.facing_left = dx < 0

        if distance < ATTACK_RANGE:
            if self.current_state != "attack":
                self.attack()
        else:
            if self.current_state != "run":
                self.set_state("run")
            dx_norm, dy_norm = dx / distance, dy / distance
            self.rect.x += dx_norm * ENEMY_SPEED
            self.rect.y += dy_norm * ENEMY_SPEED

        now = pygame.time.get_ticks()
        dt = now - self.last_update
        if dt >= self.animation_speed:
            frames_to_advance = dt // self.animation_speed
            self.frame_index += frames_to_advance

            if self.current_state == "attack":
                if self.frame_index >= len(self.frames):
                    self.set_state("run")
            else:
                self.frame_index = self.frame_index % len(self.frames)

            self.last_update = now - (dt % self.animation_speed)
            current_frame = self.frames[self.frame_index % len(self.frames)]
            self.image = pygame.transform.flip(current_frame, True, False) if self.facing_left else current_frame

def spawn_enemy(player):
    """Spawn an enemy at a random edge of the screen."""
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        x = random.randrange(0, SCREEN_WIDTH)
        y = 0
    elif edge == 'bottom':
        x = random.randrange(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT
    elif edge == 'left':
        x = 0
        y = random.randrange(0, SCREEN_HEIGHT)
    else:  # right
        x = SCREEN_WIDTH
        y = random.randrange(0, SCREEN_HEIGHT)
    return Enemy((x, y), player)
