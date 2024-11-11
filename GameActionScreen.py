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

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        # Refresh the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
