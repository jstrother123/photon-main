import pygame
import sys

def openGameActionScreen(red_team, green_team):
    pygame.init()

    # Screen size and window name
    screen_width, screen_height = 1000, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Action Screen")

    # RGB colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    NEONBLUE = (0, 255, 255)

    # Fonts
    regFont = pygame.font.Font(None, 36)
    smallFont = pygame.font.Font(None, 24)

    # Timer variables
    start_time = pygame.time.get_ticks()  # Timer start 
    countdown_time = 6 * 60 * 1000  # 6 minutes
    #countdown_time = 1 * 60 * 1000 

    clock = pygame.time.Clock()
    running = True

    #  return button after the timer ends
    show_return_button = False
    button_rect = pygame.Rect(screen_width // 2 - 200, 630, 400, 60)  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_return_button and button_rect.collidepoint(event.pos):
                    running = False

        # Calculate remaining time
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = countdown_time - elapsed_time
        if remaining_time <= 0:
            remaining_time = 0  
            show_return_button = True  

        # Convert remaining time to minutes and seconds
        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000
        timer_text = f"Time Remaining: {minutes:02}:{seconds:02}"

        # Fill background with black
        screen.fill(BLACK)

        # Draw score and game action frames
        pygame.draw.rect(screen, WHITE, (100, 25, 800, 550), 2)
        CurrScore = regFont.render("Current Score", True, NEONBLUE)
        screen.blit(CurrScore, (650, 13))

        pygame.draw.rect(screen, WHITE, (100, 325, 800, 300), 2)
        currGameAct = regFont.render("Current Game Action", True, NEONBLUE)
        screen.blit(currGameAct, (625, 313))

        # Red Team Header and Player List
        redTeamText = regFont.render("Red Team", True, WHITE)
        screen.blit(redTeamText, (250, 50))

        for i, player in enumerate(red_team):
            playerText = smallFont.render(f"{player[1]} (ID: {player[0]})", True, RED)
            screen.blit(playerText, (125, 80 + i * 30))

        # Green Team Header and Player List
        greenTeamText = regFont.render("Green Team", True, WHITE)
        screen.blit(greenTeamText, (650, 50))

        for i, player in enumerate(green_team):
            playerText = smallFont.render(f"{player[1]} (ID: {player[0]})", True, GREEN)
            screen.blit(playerText, (550, 80 + i * 30))

        # Display the timer just above the bottom white line
        timer_display = regFont.render(timer_text, True, WHITE)
        screen.blit(timer_display, (screen_width // 2 - 40, 600))

        # Display the "Return to Player Entry Screen" button if time has run out
        if show_return_button:
            pygame.draw.rect(screen, WHITE, button_rect)
            return_text = regFont.render("Return to Player Entry Screen", True, BLACK)
            screen.blit(return_text, (button_rect.x + 30, button_rect.y + 15)) 

        # Refresh the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit() 
