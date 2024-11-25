import pygame
import sys
import json

GAME_ACTIONS = []

# The max actions can be display on the game action window
MAX_ACTIONS = 8

# Record the game actions
def recordGameAction(action):
    global GAME_ACTIONS
    #print(f"Displaying GAME_ACTIONS: {GAME_ACTIONS}")
    GAME_ACTIONS.append(action)
    if len(GAME_ACTIONS) > MAX_ACTIONS:
        GAME_ACTIONS.pop(0)  # Remove the oldest action
        
    saveGameActionsToFile()
    
def saveGameActionsToFile():
    global GAME_ACTIONS
    with open('gameActions.json', 'w') as f:
        json.dump(GAME_ACTIONS, f)
       
# Read the game actions from the file
def loadGameActionsFromFile():
    try:
        with open('gameActions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # If fime not exist, return an empty array
    
def displayGameActions(screen, font, color):
    gameActions = loadGameActionsFromFile()
    y_offset = 338
    
    for action in gameActions:
        #print(f"Rendering action: {action}")
        actionText = font.render(action, True, color)
        screen.blit(actionText, (125, y_offset))
        y_offset += 30

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
    
    # Add score to the list
    redWithScores = [{"id": player[0], "name": player[1], "equipNum": player[2], "score": 0} for player in red_team]
    greenWithScores = [{"id": player[0], "name": player[1], "equipNum": player[2], "score": 0} for player in green_team]
    #print("Red Team:", redWithScores)
    #print("Green Team:", greenWithScores)
    redScoreFile(redWithScores, 'redScores.json')
    greenScoreFile(greenWithScores, 'greenScores.json')

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
                    
                    
        # Updating the score            
        redWithScores = readScore('redScores.json')
        #print(redWithScores)
        greenWithScores = readScore('greenScores.json')

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

        for i, player in enumerate(redWithScores):
            playerText = smallFont.render(f"{player['name']}(ID:{player['id']})", True, RED)
            screen.blit(playerText, (125, 80 + i * 30))
            scoreText = smallFont.render(f"{player['score']}", True, WHITE)
            screen.blit(scoreText, (410, 80 + i * 30))

        # Green Team Header and Player List
        greenTeamText = regFont.render("Green Team", True, WHITE)
        screen.blit(greenTeamText, (650, 50))

        for i, player in enumerate(greenWithScores):
            playerText = smallFont.render(f"{player['name']}(ID:{player['id']})", True, GREEN)
            screen.blit(playerText, (550, 80 + i * 30))
            scoreText = smallFont.render(f"{player['score']}", True, WHITE)
            screen.blit(scoreText, (825, 80 + i * 30)) 
            
        # Display the total scores for both team
        redTotal, greenTotal = calculateTotalScores(redWithScores, greenWithScores)
        redTotalText = regFont.render(f"Red Total: {redTotal}", True, WHITE)
        screen.blit(redTotalText, (250, 280))
        greenTotalText = regFont.render(f"Green Total: {greenTotal}", True, WHITE)
        screen.blit(greenTotalText, (650, 280))
    
        
        # Updating the game actions
        displayGameActions(screen, smallFont, WHITE)

        # Display the timer just above the bottom white line
        timer_display = regFont.render(timer_text, True, WHITE)
        screen.blit(timer_display, (screen_width // 2 - 40, 600))
        
        # Display the "Return to Player Entry Screen" button if time has run out
        if show_return_button:
            clearJsonFile('redScores.json')
            clearJsonFile('greenScores.json')
            clearJsonFile('gameActions.json')
            pygame.draw.rect(screen, WHITE, button_rect)
            return_text = regFont.render("Return to Player Entry Screen", True, BLACK)
            screen.blit(return_text, (button_rect.x + 30, button_rect.y + 15)) 

        #drawTheBase(screen, playerPos["RedPlayer1"], basePic)	
		
        # Refresh the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit() 

    
def scoring(id1, id2):
	#print("The id 1 is " + str(id1) + ", id 2 is " + str(id2))
	with open('redScores.json', 'r') as f:
		redWithScores = json.load(f)
	with open('greenScores.json', 'r') as f:
		greenWithScores = json.load(f)    
		
	if hitTeammateOrNot(id1, id2, redWithScores):
		for player in redWithScores:
			if player['equipNum'] == id1:
				player['score'] -= 10
				redScoreFile(redWithScores, 'redScores.json')
				action = f"{player['name']} shot a teammate!"
				recordGameAction(action)
	elif hitTeammateOrNot(id1, id2, greenWithScores):
		for player in greenWithScores:
			if player['equipNum'] == id1:
				player['score'] -= penalty_points
				greenScoreFile(greenWithScores, 'greenScores.json')
				action = f"{player['name']} shot a teammate!"
				recordGameAction(action)
	else:
		for player in greenWithScores:
			if player['equipNum'] == id1:
				player['score'] += 10
				greenScoreFile(greenWithScores, 'greenScores.json')
			elif player['equipNum'] == id2:
				action = f"{player['name']} been hit."
				recordGameAction(action)
				#print(action)
            
		for player in redWithScores:
			if player['equipNum'] == id1:
				player['score'] += 10
				redScoreFile(redWithScores, 'redScores.json')
			elif player['equipNum'] == id2:
				action = f"{player['name']} been hit."
				recordGameAction(action)
				#print(action)
			
def hitTeammateOrNot(id1, id2, team): # check to see if they hit the teammate
        ids = [player['equipNum'] for player in team]
        return id1 in ids and id2 in ids

  
def greenGotBase(id):
	#print(f"The id is " + str(id))
	#print("Add 100 to green")
	with open('greenScores.json', 'r') as f:
		greenWithScores = json.load(f)
	for player in greenWithScores:
		if player['equipNum'] == id:
			player['name'] = f"B {player['name']}"
			player['score'] += 100
			greenScoreFile(greenWithScores, 'greenScores.json')
			action = f"{player['name']} hit the base."
			recordGameAction(action)
			#print(action)

	
def redGotBase(id): # Need update points and add base pic\
	#print(f"The id is " + str(id))
	#print("Add 100 to red")
	with open('redScores.json', 'r') as f:
		redWithScores = json.load(f)
	for player in redWithScores:
		if player['equipNum'] == id:
			player['name'] = f"B {player['name']}"
			player['score'] += 100
			redScoreFile(redWithScores, 'redScores.json')
			#action = f"{player['name']} hit the base."
			recordGameAction(f"{player['name']} hit the base.")
    
def calculateTotalScores(redWithScores, greenWithScores):
    redTeamScores = sum(player['score'] for player in redWithScores)
    greenTeamScores = sum(player['score'] for player in greenWithScores)
    return redTeamScores, greenTeamScores    
	

def redScoreFile(redWithScores, filename='redScores.json'):
    with open(filename, 'w') as f:
        json.dump(redWithScores, f)
        #print("Red Team:", redWithScores)
    #print("Scores saved to file.")
    
def greenScoreFile(greenWithScores, filename='greenScores.json'):
    with open(filename, 'w') as f:
        json.dump(greenWithScores, f)
    #print("Scores saved to file.")


def readScore(filename):
    try:
        with open(filename, 'r') as f:
            #return json.load(f)
            data = json.load(f)
            #print(f"Data read from {filename}: {data}")
            return data
    except FileNotFoundError:
        print("error")
        return [] # If did't find anything, return empty
    
def clearJsonFile(filename): # Clear the json file
    try:
        with open(filename, 'w') as f:
            json.dump([], f)
        #print(f"{filename} has been cleared.")
    except Exception as e:
        print(f"Failed to clear {filename}: {e}")
