import copy
import pygame.draw
from board import boards
import pygame
import math

# Import modular functions
from drawing_functions import draw_misc, draw_board, draw_player
from movement_functions import check_position, move_player
from collision_functions import check_collisions
from ai_functions import get_targets
from ghost_class import Ghost
from high_score_db import HighScoreDB

pygame.init()
pygame.mixer.init()
# Dimensions of the window
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60  # frame rate
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)

color = 'blue'  # color of the line
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))

# Load sound files
pygame.mixer.set_num_channels(8)
chomp_sound = pygame.mixer.Sound('assets/sounds/pacman_chomp.wav')
death_sound = pygame.mixer.Sound('assets/sounds/pacman_death.wav')
eat_ghost_sound = pygame.mixer.Sound('assets/sounds/pacman_eatghost.wav')
eat_fruit_sound = pygame.mixer.Sound('assets/sounds/pacman_eatfruit.wav')
beginning_sound = pygame.mixer.Sound('assets/sounds/pacman_beginning.wav')
extra_pac_sound = pygame.mixer.Sound('assets/sounds/pacman_extrapac.wav')
intermission_sound = pygame.mixer.Sound('assets/sounds/pacman_intermission.wav')

# Initialize high score database
high_score_db = HighScoreDB()

# Set initial volume
pygame.mixer.music.set_volume(0.5)  # 50% volume (5/10)

player_x = 450
player_y = 663
direction = 0
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 490
pinky_y = 438
pinky_direction = 2
clyde_x = 420
clyde_y = 438
clyde_direction = 2

counter = 0
flicker = False
turns_allowed = [False, False, False, False]  # right, left, up, down
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 2
game_over = False
game_won = False
game_started = False
score_saved = False  # Track if we've saved the score to database
entering_name = False  # Track if player is entering name for top 10
player_name_input = ""  # Store the name being typed
awaiting_top_score_save = False  # Track if we need to save a top 10 score
game_paused = False  # Track if game is paused
pause_menu_selection = 0  # Current selection in pause menu (0-3)
showing_high_scores = False  # Track if viewing high scores from pause menu


















run = True
while run:  # for the time being the same is running
    timer.tick(fps)
    if not game_paused and not showing_high_scores:
        if counter < 19:
            counter += 1
            if counter > 3:
                flicker = False
        else:
            counter = 0
            flicker = True
        if powerup and power_counter < 600:
            power_counter += 1
        elif powerup and power_counter >= 600:
            power_counter = 0
            powerup = False
            eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won and not game_paused and not showing_high_scores:
        moving = False
        if not game_started:
            beginning_sound.play()
            game_started = True
        startup_counter += 1
    elif not game_paused and not showing_high_scores:
        moving = True

    screen.fill('black')  # background color
    draw_board(HEIGHT, WIDTH, level, screen, color, flicker)
    center_x = player_x + 23
    center_y = player_y + 24

    if powerup:
        ghost_speeds = [1, 1, 1, 1]  # ghost powerup speed

    else:
        ghost_speeds = [2, 2, 2, 2]  # ghost regular speed
    if eaten_ghost[0]:
        ghost_speeds[0] = 2  # if ghost eaten and came back to life
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4  # ghost eyes going back to the box
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)  # the radius of the player circle
    draw_player(direction, screen, player_images, counter, player_x, player_y)

    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                   blinky_box,
                   0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead, clyde_box, 3)

    # Update ghost collisions and draw them
    blinky.turns, blinky.in_box = blinky.check_collisions(HEIGHT, WIDTH, level)
    blinky.rect = blinky.draw(screen, powerup, eaten_ghost, spooked_img, dead_img)

    inky.turns, inky.in_box = inky.check_collisions(HEIGHT, WIDTH, level)
    inky.rect = inky.draw(screen, powerup, eaten_ghost, spooked_img, dead_img)

    pinky.turns, pinky.in_box = pinky.check_collisions(HEIGHT, WIDTH, level)
    pinky.rect = pinky.draw(screen, powerup, eaten_ghost, spooked_img, dead_img)

    clyde.turns, clyde.in_box = clyde.check_collisions(HEIGHT, WIDTH, level)
    clyde.rect = clyde.draw(screen, powerup, eaten_ghost, spooked_img, dead_img)

    # Handle high score when game ends
    high_score_info = None
    top_scores = None

    if (game_over or game_won) and not score_saved and not entering_name:
        # Check if score qualifies for top 10
        if high_score_db.is_top_10_score(score):
            entering_name = True
            awaiting_top_score_save = True
        else:
            # Not a top 10 score, just save normally
            high_score_db.update_high_score(score)
            score_saved = True

    # Always get current high score info for display during gameplay
    high_score_info = high_score_db.get_high_score_info()

    # Get top scores for leaderboard when game ends or showing high scores
    if game_over or game_won or showing_high_scores:
        top_scores = high_score_db.get_top_scores(10)

    draw_misc(font, score, screen, powerup, lives, player_images, game_over, game_won, high_score_info, top_scores, entering_name, player_name_input, game_paused, pause_menu_selection, showing_high_scores)
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y, player_x, player_y, powerup, blinky, inky, pinky, clyde, eaten_ghost)

    turns_allowed = check_position(center_x, center_y, HEIGHT, WIDTH, direction, level)
    if moving and not game_paused and not showing_high_scores:
        player_x, player_y = move_player(player_x, player_y, direction, turns_allowed, player_speed)

        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()

        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()

        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()

        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

    if not game_paused and not showing_high_scores:
        score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost, HEIGHT, WIDTH, player_x, center_y, center_x, level, chomp_sound, eat_fruit_sound)

    if not powerup and not game_paused and not showing_high_scores:

        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead):
            lives -= 1
            if lives > 0:
                death_sound.play()
                startup_counter = 0
                powerup = False
                power_counter = 0

                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 490
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 420
                clyde_y = 438
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead and not game_paused and not showing_high_scores:
        powerup = False
        power_counter = 0
        lives -= 1
        if lives > 0:
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 490
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 420
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead and not game_paused and not showing_high_scores:
        powerup = False
        power_counter = 0
        lives -= 1
        if lives > 0:
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 490
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 420
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead and not game_paused and not showing_high_scores:
        powerup = False
        power_counter = 0
        lives -= 1
        if lives > 0:
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 490
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 420
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead and not game_paused and not showing_high_scores:
        powerup = False
        power_counter = 0
        lives -= 1
        if lives > 0:
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 490
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 420
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0] and not game_paused and not showing_high_scores:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
        eat_ghost_sound.play()
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1] and not game_paused and not showing_high_scores:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
        eat_ghost_sound.play()
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2] and not game_paused and not showing_high_scores:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
        eat_ghost_sound.play()
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3] and not game_paused and not showing_high_scores:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100
        eat_ghost_sound.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # the red cross at the top
            run = False
        if event.type == pygame.KEYDOWN:
            # Handle high scores view
            if showing_high_scores:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    showing_high_scores = False
                    game_paused = True
            # Handle pause menu navigation
            elif game_paused and not entering_name:
                if event.key == pygame.K_UP:
                    pause_menu_selection = (pause_menu_selection - 1) % 4
                elif event.key == pygame.K_DOWN:
                    pause_menu_selection = (pause_menu_selection + 1) % 4
                elif event.key == pygame.K_RETURN:
                    # Handle menu selection
                    if pause_menu_selection == 0:  # Resume
                        game_paused = False
                    elif pause_menu_selection == 1:  # New Game
                        # Reset game state
                        powerup = False
                        power_counter = 0
                        startup_counter = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 490
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 420
                        clyde_y = 438
                        clyde_direction = 2
                        eaten_ghost = [False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        clyde_dead = False
                        pinky_dead = False
                        score = 0
                        lives = 2
                        level = copy.deepcopy(boards)
                        game_over = False
                        game_won = False
                        game_started = False
                        score_saved = False
                        entering_name = False
                        player_name_input = ""
                        awaiting_top_score_save = False
                        game_paused = False
                    elif pause_menu_selection == 2:  # High Scores
                        # Show high scores in-game
                        showing_high_scores = True
                        game_paused = False
                    elif pause_menu_selection == 3:  # Quit
                        run = False
                elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:  # Resume with P or ESC
                    game_paused = False
            # Handle name entry when player achieved top 10 score
            elif entering_name:
                if event.key == pygame.K_RETURN:  # Enter key to confirm name
                    # Save the score with the entered name
                    final_name = player_name_input.strip() if player_name_input.strip() else "Player"
                    high_score_db.update_high_score(score, final_name)
                    score_saved = True
                    entering_name = False
                    awaiting_top_score_save = False
                    player_name_input = ""
                elif event.key == pygame.K_BACKSPACE:  # Backspace to delete characters
                    player_name_input = player_name_input[:-1]
                elif len(player_name_input) < 12:  # Limit name length
                    # Add character to name if it's a valid character
                    if event.unicode.isalnum() or event.unicode.isspace():
                        player_name_input += event.unicode

            else:
                # Normal game controls
                if (event.key == pygame.K_p or event.key == pygame.K_ESCAPE) and not game_over and not game_won:  # Pause game
                    game_paused = True
                    pause_menu_selection = 0
                elif event.key == pygame.K_RIGHT:
                    direction_command = 0
                elif event.key == pygame.K_LEFT:
                    direction_command = 1
                elif event.key == pygame.K_UP:
                    direction_command = 2
                elif event.key == pygame.K_DOWN:
                    direction_command = 3
                if event.key == pygame.K_SPACE and (game_over or game_won):
                    powerup = False
                    power_counter = 0
                    startup_counter = 0
                    player_x = 450
                    player_y = 663
                    direction = 0
                    direction_command = 0
                    blinky_x = 56
                    blinky_y = 58
                    blinky_direction = 0
                    inky_x = 440
                    inky_y = 388
                    inky_direction = 2
                    pinky_x = 490
                    pinky_y = 438
                    pinky_direction = 2
                    clyde_x = 420
                    clyde_y = 438
                    clyde_direction = 2
                    eaten_ghost = [False, False, False, False]
                    blinky_dead = False
                    inky_dead = False
                    clyde_dead = False
                    pinky_dead = False
                    score = 0
                    lives = 2
                    level = copy.deepcopy(boards)
                    game_over = False
                    game_won = False
                    game_started = False
                    score_saved = False
                    entering_name = False
                    player_name_input = ""
                    awaiting_top_score_save = False
                    game_paused = False
                    showing_high_scores = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()
