import pygame
from settings import *
import math
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, target):
        super().__init__()
        self.target = target
        self.animations = {}
        self.load_animations()

        self.current_state = "run"
        self.frames = self.animations[self.current_state]
        self.frame_index = 0
        self.animation_speed = 50  
        self.last_update = pygame.time.get_ticks()

        self.facing_left = False
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.health = ENEMY_HP
        
        self.attack_damage = 10
        self.attack_cooldown = 500  
        self.on_cooldown = False
        self.last_attack_finished_time = 0
        self.damage_applied = False

    def load_animations(self):
        """
        Load all necessary animations into self.animations,
        keyed by state names like "run", "attack".
        Each frame is scaled up to make enemies bigger.
        """
        scale_factor = 1.5  

        run_sheet = pygame.image.load("assets/Enemy/Knight/Run.png").convert_alpha()
        run_frames = 8
        sheet_width, sheet_height = run_sheet.get_size()
        frame_width = sheet_width // run_frames
        run_frames_list = [
            run_sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
            for i in range(run_frames)
        ]
        self.animations["run"] = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in run_frames_list
        ]

        attack_sheet = pygame.image.load("assets/Enemy/Knight/Attack.png").convert_alpha()
        att_frames = 22  
        sheet_w, sheet_h = attack_sheet.get_size()
        frame_width = sheet_w // att_frames
        attack_frames_list = [
            attack_sheet.subsurface((i * frame_width, 0, frame_width, sheet_h))
            for i in range(att_frames)
        ]
        self.animations["attack"] = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in attack_frames_list
        ]
    def take_damage(self, damage):
        self.health -= damage
        print("Enemy health:", self.health)
        if self.health <= 0:
            print("Enemy died!")
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 2))

            self.kill()

    def set_state(self, new_state):
        """
        Change the current animation state, but do not interrupt
        an ongoing attack until it has finished.
        """
        if self.current_state == "attack" and new_state != "attack":
            if self.frame_index < len(self.animations["attack"]):
                return

        if new_state != self.current_state:
            self.current_state = new_state
            self.frames = self.animations[self.current_state]
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()
            self.image = (
                pygame.transform.flip(self.frames[self.frame_index], True, False)
                if self.facing_left
                else self.frames[self.frame_index]
            )
    def attack(self):
        """Start the attack state (uninterruptible)."""
        self.attack_damage = 10
        self.set_state("attack")
        self.damage_applied = False

    def update(self):
        now = pygame.time.get_ticks()
        dt = now - self.last_update

        if dt >= self.animation_speed:
            frames_to_advance = dt // self.animation_speed
            self.frame_index += frames_to_advance
            self.last_update = now - (dt % self.animation_speed)

            if self.current_state == "attack":
                if self.frame_index >= len(self.frames):
                    self.set_state("run")
                    self.last_attack_finished_time = now
                    self.on_cooldown = True
                    self.damage_applied = False
                else:
                    hit_frame = 3  # Adjust hit frame for enemy attack as needed
                    if self.frame_index == hit_frame and not self.damage_applied:
                        # Check if enemy's rect overlaps the player's rect
                        if self.rect.colliderect(self.target.rect):
                            print("Enemy attacking player!")
                            self.target.take_damage(self.attack_damage)
                        self.damage_applied = True
            else:
                self.frame_index %= len(self.frames)

            self.image = self.frames[self.frame_index % len(self.frames)]
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

        # Movement and attack decision logic
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy) or 1

        self.facing_left = dx < 0

        if not self.on_cooldown and distance < ATTACK_RANGE:
            self.attack()
        else:
            dx_norm, dy_norm = dx / distance, dy / distance
            self.rect.x += dx_norm * ENEMY_SPEED
            self.rect.y += dy_norm * ENEMY_SPEED



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
