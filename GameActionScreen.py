import pygame
import sys

def openGameActionScreen():
    pygame.init()

    # Identify the screen's size and name
    screen_width, screen_height = 1000, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Action Screen")

    # Identify the colors in RGB (use for background or font)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    #YELLOW = (255, 255, 0)
    #BLUE = (0, 0, 255)
    NEONBLUE = (0, 255, 255)

    # Indentify the font
    # Regular font to display the score
    regFont = pygame.font.Font(None, 36)
    # The smaller font to display the action did in the game
    smallFont = pygame.font.Font(None, 24)

    # Set up the game clock to control the frame rate
    clock = pygame.time.Clock()

    # Initialize the score for both teams
    redScore = 0
    greenScore = 0

    # Looping for the game
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Background color
        screen.fill(BLACK)

        # Drawing the score and the game action frame
        pygame.draw.rect(screen, WHITE, (100, 25, 800, 550), 2)
        CurrScore = regFont.render(f"Current Score", True, NEONBLUE)
        screen.blit(CurrScore, (650, 13))

        pygame.draw.rect(screen, WHITE, (100, 325, 800, 300), 2)
        currGameAct = regFont.render(f"Current Game Action", True, NEONBLUE)
        screen.blit(currGameAct, (625, 313))

        redTeamText = regFont.render(f"Red Team", True, WHITE)
        screen.blit(redTeamText, (250, 50))
        # Player's score for red team
        redPlayerText = smallFont.render(f"Player : {redScore}", True, RED)
        screen.blit(redPlayerText, (125, 80))

        greenTeamText = regFont.render(f"Green Team", True, WHITE)
        screen.blit(greenTeamText, (650, 50))
        # Player's score for green team
        GreenPlayerText = smallFont.render(f"Player: {greenScore}", True, GREEN)
        screen.blit(GreenPlayerText, (550, 80))

        # Refresh the screen
        pygame.display.flip()
        clock.tick(60)

    # Quit the game action screen
    pygame.quit()
    sys.exit()