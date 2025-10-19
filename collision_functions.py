# This file contains all collision-related functions from the original pacman.py
# No changes to the original code - just moved to separate file

def check_collisions(scor, power, power_count, eaten_ghosts, HEIGHT, WIDTH, player_x, center_y, center_x, level, chomp_sound, eat_fruit_sound):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:  # if center at regular eat point
            level[center_y // num1][center_x // num2] = 0
            scor += 10
            chomp_sound.play()
        if level[center_y // num1][center_x // num2] == 2:  # if center at power eat point
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
            eat_fruit_sound.play()

    return scor, power, power_count, eaten_ghosts