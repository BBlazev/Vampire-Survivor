import pygame

def load_heart_states():
    hearts_sheet = pygame.image.load("assets/HP/Health.png").convert_alpha()

    heart_width = 16
    heart_height = 16

    # We'll store each fill level in a list called heart_states.
    # heart_states[0] = top row (full heart)
    # heart_states[1] = 2nd row (3/4 or half heart)
    # heart_states[2] = 3rd row (1/2 or 1/4 heart)
    # heart_states[3] = bottom row (almost empty or empty heart)

    heart_states = []
    for row in range(4):
        x = 0  
        y = row * heart_height
        sub_image = hearts_sheet.subsurface((x, y, heart_width, heart_height)).copy()
        heart_states.append(sub_image)

    return heart_states

def draw_health_ui(screen, player_health, max_health, heart_states, start_pos=(10, 10)):
    heart_width = heart_states[0].get_width()
    subunits_per_heart = 4
    total_hearts = max_health // subunits_per_heart
    if max_health % subunits_per_heart != 0:
        total_hearts += 1

    x, y = start_pos

    for i in range(total_hearts):
        subunits_left = player_health - (i * subunits_per_heart)

        if subunits_left >= 4:
            heart_img = heart_states[0]
        elif subunits_left == 3:
            heart_img = heart_states[1]
        elif subunits_left == 2:
            heart_img = heart_states[2]
        elif subunits_left == 1:
            heart_img = heart_states[3]
       

        screen.blit(heart_img, (x, y))
        x += heart_width + 2

