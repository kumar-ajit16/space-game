"""
Space Game
Copyright (c) 2025 Ajit Kumar. All rights reserved.

This software is protected under copyright law and international treaties.
Unauthorized reproduction or distribution of this program, or any portion of it,
may result in severe civil and criminal penalties, and will be prosecuted to
the maximum extent possible under law.

For licensing inquiries, contact: kajit1134@gmail.com
Developer: Ajit Kumar
Version: 1.1
Release Date: 
"""

import pygame
import random
import sys
import time

# LEGAL NOTICE: This code is proprietary and confidential.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# Developed by: Ajit Kumar
# Contact: kajit1134@gmail.com

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game - © 2024 Ajit Kumar")

# COLOR DEFINITIONS
# Proprietary color scheme - do not reuse without permission
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# ASSET LOADING
# All game assets are protected by copyright
player_img = pygame.image.load('tank.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 40))

# Custom bullet design - proprietary visual element
bullet_img = pygame.Surface((7, 18), pygame.SRCALPHA)
pygame.draw.rect(bullet_img, (255, 255, 0), [0, 0, 7, 18])
bullet_speed = 9

# Enemy bullet design
enemy_bullet_img = pygame.Surface((6, 12), pygame.SRCALPHA)
pygame.draw.rect(enemy_bullet_img, RED, [0, 0, 6, 12])
enemy_bullet_speed = 5

# Enemy sprites - licensed artwork, do not redistribute
enemy_imgs = [
    pygame.transform.scale(pygame.image.load('alien1.png').convert_alpha(), (48, 36)),
    pygame.transform.scale(pygame.image.load('alien2.png').convert_alpha(), (48, 36)),
    pygame.transform.scale(pygame.image.load('alien3.png').convert_alpha(), (48, 36))
]

# FONT SETUP
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)


class Button:
    """
    Custom Button Class
    Copyright (c) 2025 Ajit Kumar. All rights reserved.
    This UI component is proprietary and may not be reused without permission.
    Developer: Ajit Kumar
    """
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (70, 130, 180)  # Proprietary color scheme
        self.highlight_color = (100, 149, 237)  # Protected visual effect

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.highlight_color, self.rect)
            if click[0] == 1:  
                return True  
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        return False


def create_enemies():
    """
    Enemy Generation Algorithm
    Proprietary game logic - protected by copyright
    Unauthorized use of this spawning mechanism is prohibited.
    Developed by: Ajit Kumar
    """
    enemies = []
    for _ in range(8):
        image = random.choice(enemy_imgs)
        x = random.randint(0, SCREEN_WIDTH - 48)
        y = random.randint(60, 160)
        speed = random.choice([2, 3, 4])
        enemies.append({
            'img': image, 
            'x': x, 
            'y': y, 
            'speed': speed,
            'last_shot': time.time(),
            'shot_cooldown': random.uniform(2.0, 5.0)
        })
    return enemies


def reset_game():
    """
    Game State Reset Function
    Copyright (c) 2025 Ajit Kumar. All rights reserved.
    This game state management system is proprietary.
    Developer: Ajit Kumar
    """
    global player_x, player_y, bullets, enemy_bullets, enemies, score, lives, game_over
    player_x = (SCREEN_WIDTH - 60) // 2
    player_y = SCREEN_HEIGHT - 70
    bullets = []
    enemy_bullets = []
    enemies = create_enemies()
    score = 0
    lives = 3
    game_over = False


def is_collision(x1, y1, x2, y2, threshold=32):
    """
    Collision Detection System
    Proprietary algorithm - protected intellectual property
    Unauthorized implementation of this collision logic is prohibited.
    Developed by: Ajit Kumar
    """
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance < threshold


# TERMS OF USE:
# This software is provided for personal use only.
# Commercial use, modification, or redistribution requires written permission.
# Contact: kajit1134@gmail.com

reset_game()

clock = pygame.time.Clock()
running = True

button_width, button_height = 200, 50
restart_button = Button((SCREEN_WIDTH - button_width)//2, SCREEN_HEIGHT//2 + 50, button_width, button_height, "Restart")

# MAIN GAME LOOP
# Core game engine - proprietary technology
# Developed by: Ajit Kumar
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()

        # Player controls - proprietary input handling system
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 6
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 60:
            player_x += 6

        # Weapon system - protected game mechanic
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                bullets.append([player_x + 28, player_y])

        # Bullet management - proprietary physics system
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            screen.blit(bullet_img, (bullet[0], bullet[1]))
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Enemy bullet management
        current_time = time.time()
        for enemy in enemies:
            # Enemy shooting logic
            if current_time - enemy['last_shot'] > enemy['shot_cooldown']:
                enemy_bullets.append([enemy['x'] + 24, enemy['y'] + 36])
                enemy['last_shot'] = current_time
                enemy['shot_cooldown'] = random.uniform(2.0, 5.0)

        # Update enemy bullets
        for e_bullet in enemy_bullets[:]:
            e_bullet[1] += enemy_bullet_speed
            screen.blit(enemy_bullet_img, (e_bullet[0], e_bullet[1]))
            if e_bullet[1] > SCREEN_HEIGHT:
                enemy_bullets.remove(e_bullet)

            # Check collision with player
            if is_collision(e_bullet[0], e_bullet[1], player_x + 30, player_y + 20, threshold=30):
                enemy_bullets.remove(e_bullet)
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # Reset player position and clear bullets on hit
                    player_x = (SCREEN_WIDTH - 60) // 2
                    bullets.clear()
                    enemy_bullets.clear()
                    pygame.display.update()
                    time.sleep(1)
                break

        # Enemy AI and movement - protected algorithm
        for enemy in enemies:
            enemy['x'] += enemy['speed']
            if enemy['x'] <= 0 or enemy['x'] >= SCREEN_WIDTH - 48:
                enemy['speed'] = -enemy['speed']
                enemy['y'] += 40
            screen.blit(enemy['img'], (enemy['x'], enemy['y']))

            # Combat system - proprietary game mechanics
            for bullet in bullets[:]:
                if is_collision(enemy['x'] + 24, enemy['y'] + 18, bullet[0], bullet[1]):
                    if bullet in bullets:
                        bullets.remove(bullet)

                    enemy['x'] = random.randint(0, SCREEN_WIDTH - 48)
                    enemy['y'] = random.randint(60, 160)
                    enemy['speed'] = random.choice([2, 3, 4])
                    enemy['img'] = random.choice(enemy_imgs)
                    enemy['last_shot'] = current_time
                    enemy['shot_cooldown'] = random.uniform(2.0, 5.0)
                    score += 1

            # Enemy collision with player - enhanced damage system
            if is_collision(enemy['x'] + 24, enemy['y'] + 18, player_x + 30, player_y + 20, threshold=40):
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    player_x = (SCREEN_WIDTH - 60) // 2
                    bullets.clear()
                    enemy_bullets.clear()
                    enemies = create_enemies()
                    pygame.display.update()
                    time.sleep(1)
                break

        screen.blit(player_img, (player_x, player_y))

        # UI System - proprietary interface design
        score_lives = font.render(f"Score: {score}   Lives: {lives}", True, WHITE)
        screen.blit(score_lives, (10, 10))

    else:
        # Game over screen - protected UI design
        game_over_text = big_font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, SCREEN_HEIGHT // 2))

        if restart_button.draw(screen):
            reset_game()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()

"""
END OF FILE - PROPRIETARY CODE

LEGAL DISCLAIMER:
This software and its source code are the intellectual property of Ajit Kumar.
Any unauthorized use, reproduction, or distribution may violate copyright, trademark,
and other laws. Violators will be subject to legal action.

This product is licensed, not sold. By using this software, you agree to the terms
of the license agreement.

Developer: Ajit Kumar
Contact: kajit1134@gmail.com
Patent Pending: Various game mechanics and systems implemented herein.

All rights reserved. Distribution prohibited without explicit written permission.
"""