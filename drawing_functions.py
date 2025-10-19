import pygame
import math

PI = math.pi

def draw_misc(font, score, screen, powerup, lives, player_images, game_over, game_won, high_score_info=None, top_scores=None, entering_name=False, player_name_input="", game_paused=False, pause_menu_selection=0, showing_high_scores=False):
    score_text = font.render(f'Score:{score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

    # Display high score in bottom right corner during gameplay
    if high_score_info and not game_over and not game_won and not game_paused and not showing_high_scores:
        high_score_text = font.render(f'High Score: {high_score_info["score"]}', True, 'white')
        screen.blit(high_score_text, (720, 920))

    # Display pause controls hint during gameplay
    if not game_over and not game_won and not game_paused and not showing_high_scores and not entering_name:
        
        smaller_font = pygame.font.Font('freesansbold.ttf', 19)
        pause_hint = smaller_font.render("P or ESC to pause", True, 'gray')
        screen.blit(pause_hint, (22, 20))

    if game_over:
        if entering_name:
            # Name entry screen
            pygame.draw.rect(screen, 'white', [200, 300, 500, 200], 0, 10)
            pygame.draw.rect(screen, 'black', [220, 320, 460, 160], 0, 10)

            congrats_text = font.render("TOP 10 SCORE!", True, 'gold')
            screen.blit(congrats_text, (350, 340))

            name_prompt_text = font.render("Enter your name:", True, 'white')
            screen.blit(name_prompt_text, (340, 370))


            # Show current input box with background
            pygame.draw.rect(screen, 'white', [280, 400, 340, 30], 0)  # Fill background
            pygame.draw.rect(screen, 'black', [280, 400, 340, 30], 2)  # Border

            # Show the input text or placeholder with cursor
            display_text = player_name_input if player_name_input else "Type your name..."
            if player_name_input:
                display_text += "|"  # Add cursor when typing
            text_color = 'black' if player_name_input else 'gray'
            name_text = font.render(display_text, True, text_color)
            screen.blit(name_text, (285, 405))

            instruction_text = font.render("Press ENTER to confirm", True, 'gray')
            screen.blit(instruction_text, (320, 440))
        else:
            # Normal game over screen with leaderboard
            pygame.draw.rect(screen, 'white', [50, 100, 800, 650], 0, 10)
            pygame.draw.rect(screen, 'black', [70, 120, 760, 610], 0, 10)

            gameover_text = font.render("Game Over! Press SPACE BAR to restart!", True, 'red')
            screen.blit(gameover_text, (250, 150))

            # Display current score
            current_score_text = font.render(f"Your Score: {score}", True, 'white')
            screen.blit(current_score_text, (350, 180))

            # Display if new high score
            if high_score_info and score > high_score_info['score']:
                high_score_text = font.render("NEW HIGH SCORE!", True, 'gold')
                screen.blit(high_score_text, (350, 210))

            # Display top 10 leaderboard
            if top_scores:
                leaderboard_title = font.render("*** TOP 10 LEADERBOARD ***", True, 'yellow')
                screen.blit(leaderboard_title, (300, 250))

                for i, score_data in enumerate(top_scores[:10], 1):
                    y_pos = 280 + (i * 30)
                    rank_display = "1." if i == 1 else "2." if i == 2 else "3." if i == 3 else f"{i:2d}."

                    # Highlight current player's score
                    color = 'lime' if score_data['score'] == score else 'white'

                    score_line = f"{rank_display:>4} {score_data['score']:>6} pts  {score_data['player']:<12}"
                    score_text = font.render(score_line, True, color)
                    screen.blit(score_text, (150, y_pos))

    if game_won:
        if entering_name:
            # Name entry screen
            pygame.draw.rect(screen, 'white', [200, 300, 500, 200], 0, 10)
            pygame.draw.rect(screen, 'black', [220, 320, 460, 160], 0, 10)

            congrats_text = font.render("TOP 10 SCORE!", True, 'gold')
            screen.blit(congrats_text, (350, 340))

            name_prompt_text = font.render("Enter your name:", True, 'white')
            screen.blit(name_prompt_text, (340, 370))


            # Show current input box with background
            pygame.draw.rect(screen, 'white', [280, 400, 340, 30], 0)  # Fill background
            pygame.draw.rect(screen, 'black', [280, 400, 340, 30], 2)  # Border

            # Show the input text or placeholder with cursor
            display_text = player_name_input if player_name_input else "Type your name..."
            if player_name_input:
                display_text += "|"  # Add cursor when typing
            text_color = 'black' if player_name_input else 'gray'
            name_text = font.render(display_text, True, text_color)
            screen.blit(name_text, (285, 405))

            instruction_text = font.render("Press ENTER to confirm", True, 'gray')
            screen.blit(instruction_text, (320, 440))
        else:
            # Normal victory screen with leaderboard
            pygame.draw.rect(screen, 'white', [50, 100, 800, 650], 0, 10)
            pygame.draw.rect(screen, 'black', [70, 120, 760, 610], 0, 10)

            gameover_text = font.render("Victory! Press SPACE BAR to restart!", True, 'green')
            screen.blit(gameover_text, (250, 150))

            # Display current score
            current_score_text = font.render(f"Your Score: {score}", True, 'white')
            screen.blit(current_score_text, (350, 180))

            # Display if new high score
            if high_score_info and score > high_score_info['score']:
                high_score_text = font.render("NEW HIGH SCORE!", True, 'gold')
                screen.blit(high_score_text, (350, 210))

            # Display top 10 leaderboard
            if top_scores:
                leaderboard_title = font.render("*** TOP 10 LEADERBOARD ***", True, 'yellow')
                screen.blit(leaderboard_title, (300, 250))

                for i, score_data in enumerate(top_scores[:10], 1):
                    y_pos = 280 + (i * 30)
                    rank_display = f"{i}"

                    # Highlight current player's score
                    color = 'lime' if score_data['score'] == score else 'white'

                    score_line = f"{rank_display:>4} {score_data['score']:>6} pts  {score_data['player']:<12}"
                    score_text = font.render(score_line, True, color)
                    screen.blit(score_text, (150, y_pos))

    # Pause menu
    if game_paused:
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 950))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Pause menu background
        pygame.draw.rect(screen, 'white', [200, 250, 500, 400], 0, 10)
        pygame.draw.rect(screen, 'black', [220, 270, 460, 360], 0, 10)

        # Title (centered)
        pause_title = font.render("GAME PAUSED", True, 'yellow')
        title_rect = pause_title.get_rect(center=(450, 320))
        screen.blit(pause_title, title_rect)

        # Menu options
        menu_options = [
            "Resume Game",
            "New Game",
            "High Scores",
            "Quit Game"
        ]

        for i, option in enumerate(menu_options):
            y_pos = 380 + (i * 50)
            color = 'lime' if i == pause_menu_selection else 'white'

            # Highlight selected option
            if i == pause_menu_selection:
                pygame.draw.rect(screen, 'gray', [300, y_pos - 5, 300, 40], 0, 5)

            option_text = font.render(option, True, color)
            # Center the text
            text_rect = option_text.get_rect(center=(450, y_pos + 15))
            screen.blit(option_text, text_rect)

        # Instructions (centered)
        instruction_text = font.render("ENTER to select, P or ESC to resume", True, 'gray')
        instruction_rect = instruction_text.get_rect(center=(450, 600))
        screen.blit(instruction_text, instruction_rect)

    # High Scores display (when viewing from pause menu)
    if showing_high_scores:
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 950))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # High scores background
        pygame.draw.rect(screen, 'white', [100, 150, 700, 600], 0, 10)
        pygame.draw.rect(screen, 'black', [120, 170, 660, 560], 0, 10)

        # Title
        title_text = font.render("*** HIGH SCORES ***", True, 'yellow')
        screen.blit(title_text, (375, 190))

        # Display top scores
        if top_scores:
            for i, score_data in enumerate(top_scores[:10], 1):
                y_pos = 240 + (i * 35)
                rank_display = f"{i}"

                score_line = f"{rank_display:>4} {score_data['score']:>6} pts  {score_data['player']:<12}  {score_data['date']}"
                score_text = font.render(score_line, True, 'white')
                screen.blit(score_text, (140, y_pos))
        else:
            no_scores_text = font.render("No scores recorded yet!", True, 'gray')
            screen.blit(no_scores_text, (375, 400))

        # Instructions (centered)
        back_instruction = font.render("Press ESC or P to return to pause menu", True, 'gray')
        back_rect = back_instruction.get_rect(center=(450, 680))
        screen.blit(back_instruction, back_rect)


def draw_board(HEIGHT, WIDTH, level, screen, color, flicker):
    num1 = ((HEIGHT - 50) // 32)  # 50px padding at the bottom for the stats
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player(direction, screen, player_images, counter, player_x, player_y):
    if direction == 0:  # right
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:  # left
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:  # up
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:  # down
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))