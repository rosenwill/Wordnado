# Wordnado Current Development

import pygame, sys, random
from pygame.locals import *
from PyDictionary import PyDictionary
import string, time, math

pygame.init()

# Game Constants

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

dictionary = PyDictionary()

WIDTH = 400 #600
HEIGHT = 600 #900

player = pygame.transform.scale(pygame.image.load('Images/Sprites/reggie.png'), (64, 64))

bg_img = pygame.image.load('Images/Backgrounds/tornado.jpg')
fps = 60
timer = pygame.time.Clock()


platform = pygame.image.load('Images/Elements/cloud2.png')
platform = pygame.transform.scale(platform, (140, 60))

stop_button = pygame.Surface((75, 35))
stop_button.fill((175, 52, 52))

screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
pygame.display.set_caption('Wordnado')

# Music Variables

pygame.mixer.init()
pygame.mixer.music.load("Sounds/music.mp3")
pygame.mixer.music.set_volume(0.7)
jump_sound = pygame.mixer.Sound("Sounds/jumpSound.mp3")


# Game Variables

player_x = 175
player_y = 450
platforms = [
	[145, 500, 105, 15],
	[40,  300, 105, 15],
	[285, 100, 105, 15],
	[105, 200, 105, 15]
]

condition = {
	0: False,
	1: False,
	2: False,
	3: False,
}

letter_holding = [
	None,
	None,
	None,
	None,
]

jump = False
y_change = 0
x_change = 0
player_speed = 4.5
inputMap = [False, False]

# Update Players Y-Position

def update_player(y_pos):
	global jump
	global y_change
	jump_height = 16.5
	gravity = .65

	if jump:
		y_change = -jump_height
		jump = False

	y_pos += y_change
	if y_change < 14:
		y_change += gravity

	if y_pos < -25:
		y_pos = y_pos - (y_pos + 25)

	return y_pos

# Check for Collisions

def check_collisions(rect_list, j):
	global player_x
	global player_y
	global y_change
	for i in range(len(rect_list)):
		if rect_list[i].colliderect([player_x + 24, player_y + 60, 20, 8]) and jump == False and y_change > 0:
			pygame.mixer.Sound.play(jump_sound)
			j = True
	return j

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)
scoreX = 8
scoreY = 8
recentX = 8
recentY = 40

# Letters
collected_letters = []
num_collected = 0
letter_font = pygame.font.Font('freesansbold.ttf', 36)
stop_text = font.render("STOP", True, (255, 255, 255))
collectX = 8
collectY = 40

# Random letters
vowels = ["A", "E", "I", "O", "U"]
consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]
def create_letter():
    if random.random() < 0.25:
        return random.choice(vowels)
    else:
        return random.choice(consonants)

# Check if the word is real.

def is_word(word):
	if dictionary.meaning(word, True) is None:
		return False
	else:
		return True

# Time Limit / Clock
clock = pygame.time.Clock()
start_time = time.time()
counter = 45
timeX = WIDTH - 50
timeY = 10
pygame.time.set_timer(pygame.USEREVENT, 45)
font = pygame.font.Font('freesansbold.ttf', 28)

# Handle Platform Movement

def update_platforms(platform_list, pos, change):
	if pos < 300 and change < 0:
		for i in range(len(platform_list)):
			platform_list[i][1] += -change
	elif (pos < 100 and change < 0) or (pos < 5):
		for i in range(len(platform_list)):
			platform_list[i][1] += 10
	else:
		pass
	for item in range(len(platform_list)):
		if platform_list[item][1] > 600:
			condition[item] = False
			platform_list[item] = [random.randint(5, 300), 0, 105, 15]
			if random.randint(0, 100) < 40:
				condition[item] = True
				letter_holding[item] = create_letter()
					
	return platform_list

def display_score():
	screen.blit(font.render("Score: " + str(score_value), True, white), (scoreX, scoreY))

def display_recent():
	if len(collected_letters) > 4:
		recent_letters = collected_letters[-4:][::-1]
	else:
		recent_letters = collected_letters[::-1]
	recent_letters_text = "Recent: " + " ".join(recent_letters)
	recent_letters_render = font.render(recent_letters_text, True, white)
	screen.blit(recent_letters_render, (recentX, recentY))

def display_text(text, x, y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text_surface, text_rect)

# Run Game

makeLetter = False
running = True
while running == True:
	pygame.mixer.music.play()
	exit = False
	while True:
		timer.tick(fps)
		screen.blit(bg_img, (0, 0))
		screen.blit(player, (player_x, player_y))
		blocks = []

		# Level Over Screen Set-Up
		endText = pygame.font.Font('freesansbold.ttf', 40).render('Level Over', True, (174, 201, 220))
		retry1Text = pygame.font.Font('freesansbold.ttf', 14).render('Press the R key to restart', True, (174, 201, 220))
		retry2Text = pygame.font.Font('freesansbold.ttf', 14).render('or press Enter to exit the level', True, (174, 201, 220))
		border = pygame.Rect(0, 0, (WIDTH // 3) * 2, (HEIGHT // 3))
		border.center = (WIDTH / 2, HEIGHT / 2)
		endTextRect = endText.get_rect()
		endTextRect.center = border.center
		endTextRect.y = endTextRect.y - 30
		retry1TextRect, retry2TextRect = retry1Text.get_rect(), retry2Text.get_rect()
		retry1TextRect.center = retry2TextRect.center = border.center
		retry1TextRect.y, retry2TextRect.y = retry1TextRect.y + 20, retry2TextRect.y + 45

		for i in range(len(platforms)):
			block = pygame.draw.rect(screen, black, platforms[i], 0, 15)
			screen.blit(platform, (block.x - 17, block.y - 25))
			if condition[i] == True: # Letter 
				letter_text = letter_font.render(letter_holding[i], True, (255, 255, 255))
				screen.blit(letter_text, (block.x + 52.5 - letter_text.get_width()/2, block.y - 60))

				if letter_text:
					if player_x < block.x + 105 and player_x + 64 > block.x:
						if player_y < block.y + 15 and player_y + 64 > block.y:
							collected_letters.append(letter_holding[i])
							num_collected += 1
							score_value += 10
							condition[i] = False

			blocks.append(block)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:    
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					inputMap[0] = True;
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					inputMap[1] = True;
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					inputMap[0] = False;
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					inputMap[1] = False;
			if event.type == pygame.USEREVENT: # timer
				counter -= fps / 2000

		if inputMap[0]: x_change = -player_speed
		if inputMap[1]: x_change = player_speed
		if not inputMap[0] and not inputMap[1]: x_change = 0

		display_score()
		display_recent()

		# Display timer
		screen.blit(font.render("0" if counter <= 0 else str(round(counter)), True, white), (timeX if counter >= 9.5 else timeX + 20, timeY))
		pygame.display.flip()
		if counter < 0:
			makeLetter = True
			break

		player_y = update_player(player_y)
		player_x += x_change
		jump = check_collisions(blocks, jump)
		platforms = update_platforms(platforms, player_y, y_change)

		if x_change > 0:
			player = pygame.transform.scale(pygame.image.load('Images/Sprites/reggie.png'), (64, 64))
		elif x_change < 0:
			player = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Images/Sprites/reggie.png'), (64, 64)), 1, 0)

		if player_y > HEIGHT:
			if num_collected > 0:
				makeLetter = True
			break

		for item in range(len(platforms)):
			if condition[item] == True:
				pass

		pygame.display.update()

	while makeLetter:

		stop = False
		stop_button_rect = stop_button.get_rect()
		stop_button_rect.bottomright = (WIDTH - 10, HEIGHT - 10)

		if num_collected > 0:
			collected_letters_copy = collected_letters.copy() # create a copy of the collected letters
			word_input = ""
			word_input_rect = pygame.Rect(WIDTH/4, (HEIGHT/2) - 50, WIDTH/2, 30)
			start_time = time.time() # reset the start time
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						if stop_button_rect.collidepoint(event.pos):
							stop = True
							break
					if num_collected == 0:
						stop = True
						break
					if event.type == pygame.KEYDOWN:
						if event.unicode.isalnum() and len(word_input) < 9:
							word_input += event.unicode.upper() # convert input to uppercase
						elif event.key == K_BACKSPACE:
							word_input = word_input[:-1]
						elif event.key == K_RETURN:
							if len(word_input) < 2 or len(word_input) > 9:
								continue
							if all(letter in collected_letters_copy for letter in word_input) and len(word_input) <= len(collected_letters_copy):
								if is_word(word_input):
									for letter in word_input:
										num_collected -= 1
										collected_letters_copy.remove(letter) # remove used letters from the copy
									score_value += (len(word_input) * 100) # award points based on word length
									word_input = ""
									break
								else:
									pass
							else:
								pass
				if stop == True:
					makeLetter = False
					break
				if time.time() - start_time > 45: # check if time limit has been exceeded
					makeLetter = False
					break
				screen.blit(bg_img, (0, 0)) # keep the tornado background
				pygame.draw.rect(screen, white, word_input_rect, 2)
				word_input_image = font.render(word_input, True, white)
				screen.blit(word_input_image, (word_input_rect.x + 5, word_input_rect.y + 2.5))
				# Display Letters
				currRow = 0
				defHeight = 30
				for num in range(math.ceil(len(collected_letters_copy) / 10)):
					collected_letters_cc = collected_letters_copy[currRow:(currRow + 10)]
					letters = ' '.join(collected_letters_cc)
					letters_image = font.render(letters, True, white)
					letters_image_rect = letters_image.get_rect()
					letters_image_rect.center = (WIDTH/2, HEIGHT/2 + defHeight)
					screen.blit(letters_image, letters_image_rect)
					currRow += 10
					defHeight += 40

				display_score()
				screen.blit(stop_button, stop_button_rect)
				screen.blit(stop_text, (stop_button_rect[0] + 5, stop_button_rect[1] + 5))
				# Display Time
				time_remaining = int(45 - (time.time() - start_time))
				time_text = str(time_remaining)
				time_image = font.render(time_text, True, (255, 255, 255))
				screen.blit(time_image, (timeX, timeY))
				pygame.display.update()

	while not exit:

		# Replay screen
		inputMap = [False, False]
		pygame.draw.rect(screen, (90, 108, 122), border)
		pygame.draw.rect(screen, (43, 50, 54), border, 5)
		screen.blit(endText, endTextRect)
		screen.blit(retry1Text, retry1TextRect)
		screen.blit(retry2Text, retry2TextRect)

		# Retry options -> R key and Enter key
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == K_r: # R Key = Restart level
					exit = True
					# Reset changed values to default values
					collected_letters = []
					num_collected = 0
					score_value = 0
					player_x = 175
					player_y = 420
					timeX = WIDTH - 50
					counter = 45
					game_over = False
					platforms = [
						[145, 500, 105, 15],
						[40,  300, 105, 15],
						[285, 100, 105, 15],]
				elif event.key == pygame.K_RETURN: # Enter Key = Exit level
					exit = True
					running = False

		pygame.display.update()

pygame.quit()